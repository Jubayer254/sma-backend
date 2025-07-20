import re
import boto3
from botocore.exceptions import ClientError

from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from course_material.models.recording import Recording
from course_material.models.class_resources import ClassResource
from course_material.models.course import Course

from django.conf import settings

MINIO_ENDPOINT = settings.MINIO_ENDPOINT
MINIO_ACCESS_KEY = settings.MINIO_ACCESS_KEY
MINIO_SECRET_KEY = settings.MINIO_SECRET_KEY
MINIO_BUCKET_NAME = settings.MINIO_BUCKET_NAME


def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    )


def parse_range_header(range_header, file_size):
    """
    Parse HTTP Range header.
    Returns (start, end) byte positions or None if invalid.
    """
    range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)
    if range_match:
        start = int(range_match.group(1))
        end = range_match.group(2)
        end = int(end) if end else file_size - 1
        if end >= file_size:
            end = file_size - 1
        if start > end:
            return None
        return start, end
    return None


class SecureRecordingDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            recording = Recording.objects.get(pk=pk)

            if not recording.batch.enrollments.filter(student=request.user).exists():
                return Response({"detail": "Access denied"}, status=403)

            s3 = get_s3_client()
            meta = s3.head_object(Bucket=MINIO_BUCKET_NAME, Key=recording.recording_file.name)
            file_size = meta['ContentLength']
            content_type = meta['ContentType']

            range_header = request.headers.get('Range', '').strip()
            if range_header:
                byte_range = parse_range_header(range_header, file_size)
                if byte_range:
                    start, end = byte_range
                    length = end - start + 1

                    s3_object = s3.get_object(
                        Bucket=MINIO_BUCKET_NAME,
                        Key=recording.recording_file.name,
                        Range=f'bytes={start}-{end}'
                    )

                    response = StreamingHttpResponse(
                        streaming_content=s3_object['Body'].iter_chunks(),
                        status=206,
                        content_type=content_type
                    )
                    response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
                    response['Accept-Ranges'] = 'bytes'
                    response['Content-Length'] = str(length)
                    response['Content-Disposition'] = f'attachment; filename="{recording.recording_file.name.split("/")[-1]}"'
                    return response

            # No Range header - send whole file
            s3_object = s3.get_object(Bucket=MINIO_BUCKET_NAME, Key=recording.recording_file.name)
            response = StreamingHttpResponse(
                streaming_content=s3_object['Body'].iter_chunks(),
                content_type=content_type
            )
            response['Content-Length'] = str(file_size)
            response['Accept-Ranges'] = 'bytes'
            response['Content-Disposition'] = f'attachment; filename="{recording.recording_file.name.split("/")[-1]}"'
            return response

        except Recording.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)
        except ClientError as e:
            return Response({"detail": "MinIO error", "error": str(e)}, status=500)


class SecureResourceDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            resource = ClassResource.objects.get(pk=pk)

            if not resource.batch.enrollments.filter(student=request.user).exists():
                return Response({"detail": "Access denied"}, status=403)

            if not resource.file:
                return Response({"detail": "No file uploaded"}, status=404)

            s3 = get_s3_client()
            meta = s3.head_object(Bucket=MINIO_BUCKET_NAME, Key=resource.file.name)
            file_size = meta['ContentLength']
            content_type = meta['ContentType']

            range_header = request.headers.get('Range', '').strip()
            if range_header:
                byte_range = parse_range_header(range_header, file_size)
                if byte_range:
                    start, end = byte_range
                    length = end - start + 1

                    s3_object = s3.get_object(
                        Bucket=MINIO_BUCKET_NAME,
                        Key=resource.file.name,
                        Range=f'bytes={start}-{end}'
                    )

                    response = StreamingHttpResponse(
                        streaming_content=s3_object['Body'].iter_chunks(),
                        status=206,
                        content_type=content_type
                    )
                    response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
                    response['Accept-Ranges'] = 'bytes'
                    response['Content-Length'] = str(length)
                    response['Content-Disposition'] = f'attachment; filename="{resource.file.name.split("/")[-1]}"'
                    return response

            # No Range header - send whole file
            s3_object = s3.get_object(Bucket=MINIO_BUCKET_NAME, Key=resource.file.name)
            response = StreamingHttpResponse(
                streaming_content=s3_object['Body'].iter_chunks(),
                content_type=content_type
            )
            response['Content-Length'] = str(file_size)
            response['Accept-Ranges'] = 'bytes'
            response['Content-Disposition'] = f'attachment; filename="{resource.file.name.split("/")[-1]}"'
            return response

        except ClassResource.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)
        except ClientError as e:
            return Response({"detail": "MinIO error", "error": str(e)}, status=500)


class PublicDemoVideoView(APIView):
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            if not course.demo_video:
                return Response({"detail": "No demo video found"}, status=404)

            s3 = get_s3_client()
            meta = s3.head_object(Bucket=MINIO_BUCKET_NAME, Key=course.demo_video.name)
            file_size = meta['ContentLength']
            content_type = meta['ContentType']

            range_header = request.headers.get('Range', '').strip()
            if range_header:
                byte_range = parse_range_header(range_header, file_size)
                if byte_range:
                    start, end = byte_range
                    length = end - start + 1

                    s3_object = s3.get_object(
                        Bucket=MINIO_BUCKET_NAME,
                        Key=course.demo_video.name,
                        Range=f'bytes={start}-{end}'
                    )

                    response = StreamingHttpResponse(
                        streaming_content=s3_object['Body'].iter_chunks(),
                        status=206,
                        content_type=content_type
                    )
                    response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
                    response['Accept-Ranges'] = 'bytes'
                    response['Content-Length'] = str(length)
                    response['Content-Disposition'] = f'inline; filename="{course.demo_video.name.split("/")[-1]}"'
                    return response

            # No Range header - send whole file
            s3_object = s3.get_object(Bucket=MINIO_BUCKET_NAME, Key=course.demo_video.name)
            response = StreamingHttpResponse(
                streaming_content=s3_object['Body'].iter_chunks(),
                content_type=content_type
            )
            response['Content-Length'] = str(file_size)
            response['Accept-Ranges'] = 'bytes'
            response['Content-Disposition'] = f'inline; filename="{course.demo_video.name.split("/")[-1]}"'
            return response

        except Course.DoesNotExist:
            return Response({"detail": "Course not found"}, status=404)
        except ClientError as e:
            return Response({"detail": "MinIO error", "error": str(e)}, status=500)
