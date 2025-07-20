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

# your MinIO config
MINIO_ENDPOINT = settings.MINIO_ENDPOINT
MINIO_ACCESS_KEY = settings.MINIO_ACCESS_KEY
MINIO_SECRET_KEY = settings.MINIO_SECRET_KEY
MINIO_BUCKET_NAME = settings.MINIO_BUCKET_NAME
USE_HTTPS = settings.USE_HTTPS

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=f"{'https' if USE_HTTPS else 'http'}://{MINIO_ENDPOINT}",
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    )

class SecureRecordingDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            recording = Recording.objects.get(pk=pk)

            # Optional: enforce user permission
            if not recording.batch.enrollments.filter(student=request.user).exists():
                return Response({"detail": "Access denied"}, status=403)

            s3 = get_s3_client()
            s3_object = s3.get_object(Bucket=MINIO_BUCKET_NAME, Key=recording.recording_file.name)
            response = StreamingHttpResponse(
                streaming_content=s3_object['Body'].iter_chunks(),
                content_type=s3_object['ContentType']
            )
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

            # Optional: enforce user permission
            if not resource.batch.enrollments.filter(student=request.user).exists():
                return Response({"detail": "Access denied"}, status=403)

            if not resource.file:
                return Response({"detail": "No file uploaded"}, status=404)

            s3 = get_s3_client()
            s3_object = s3.get_object(Bucket=MINIO_BUCKET_NAME, Key=resource.file.name)
            response = StreamingHttpResponse(
                streaming_content=s3_object['Body'].iter_chunks(),
                content_type=s3_object['ContentType']
            )
            response['Content-Disposition'] = f'attachment; filename="{resource.file.name.split("/")[-1]}"'
            return response

        except ClassResource.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)
        except ClientError as e:
            return Response({"detail": "MinIO error", "error": str(e)}, status=500)

class PublicDemoVideoView(APIView):
    # No permission_classes means open access (public)
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            if not course.demo_video:
                return Response({"detail": "No demo video found"}, status=404)

            s3 = get_s3_client()
            s3_object = s3.get_object(Bucket=MINIO_BUCKET_NAME, Key=course.demo_video.name)

            response = StreamingHttpResponse(
                streaming_content=s3_object['Body'].iter_chunks(),
                content_type=s3_object['ContentType']
            )
            response['Content-Disposition'] = f'inline; filename="{course.demo_video.name.split("/")[-1]}"'
            return response

        except Course.DoesNotExist:
            return Response({"detail": "Course not found"}, status=404)
        except ClientError as e:
            return Response({"detail": "MinIO error", "error": str(e)}, status=500)