# course_material/views.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import StreamingHttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from course_material.models.recording import Recording
from course_material.models.class_resources import ClassResource
from course_material.models.course import Course
from course_material.models.enrollment import Enrollment
from django.conf import settings
import requests
from course_material.minio_backend import get_s3_client
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


def generate_presigned_url(object_key):
    s3 = get_s3_client()
    return s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': settings.MINIO_BUCKET_NAME, 'Key': object_key},
        ExpiresIn=3600
    )


def proxy_minio_file_response(presigned_url, request):
    headers = {}
    if 'Range' in request.headers:
        headers['Range'] = request.headers['Range']

    r = requests.get(presigned_url, stream=True, headers=headers)
    if r.status_code not in [200, 206]:
        return HttpResponseNotFound("File not found or expired")

    resp = StreamingHttpResponse(r.iter_content(chunk_size=8192), status=r.status_code)
    resp['Content-Type'] = r.headers.get('Content-Type', 'application/octet-stream')
    resp['Content-Length'] = r.headers.get('Content-Length', '')
    if 'Content-Range' in r.headers:
        resp['Content-Range'] = r.headers['Content-Range']
    resp['Accept-Ranges'] = 'bytes'
    return resp


class ProxyDemoVideoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if not course.demo_video_object_key:
            return HttpResponseNotFound("No demo video found")

        presigned_url = generate_presigned_url(course.demo_video_object_key)
        return proxy_minio_file_response(presigned_url, request)


class ProxyRecordingView(APIView):
    permission_classes = [AllowAny]  # We'll handle auth manually

    def get(self, request, pk):
        # Get token from query param
        token = request.GET.get('token')
        if not token:
            return HttpResponseForbidden("Missing token")

        # Validate token
        try:
            validated_token = JWTAuthentication().get_validated_token(token)
            user = JWTAuthentication().get_user(validated_token)
        except InvalidToken:
            return HttpResponseForbidden("Invalid token")

        # Attach user to request for permission check
        request.user = user

        # Fetch recording
        recording = get_object_or_404(Recording, pk=pk)

        # Check if user is enrolled in the batch
        if not Enrollment.objects.filter(batch=recording.batch, student=user).exists():
            return HttpResponseForbidden("You do not have access to this recording")

        # Generate presigned URL for MinIO object
        presigned_url = generate_presigned_url(recording.object_key)

        # Forward Range header if exists
        headers = {}
        range_header = request.headers.get('Range')
        if range_header:
            headers['Range'] = range_header

        # Fetch the file from MinIO with Range support
        r = requests.get(presigned_url, stream=True, headers=headers)

        if r.status_code not in [200, 206]:
            return HttpResponseNotFound("File not found or expired")

        response = StreamingHttpResponse(r.iter_content(chunk_size=8192), status=r.status_code)
        response['Content-Type'] = r.headers.get('Content-Type', 'application/octet-stream')
        response['Content-Length'] = r.headers.get('Content-Length', '')
        if 'Content-Range' in r.headers:
            response['Content-Range'] = r.headers['Content-Range']
        response['Accept-Ranges'] = 'bytes'

        return response


class ProxyResourceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        resource = get_object_or_404(ClassResource, pk=pk)

        # Check if user is enrolled in the batch
        if not Enrollment.objects.filter(batch=resource.batch, student=request.user).exists():
            return HttpResponseForbidden("You do not have access to this resource")

        presigned_url = generate_presigned_url(resource.object_key)
        if not presigned_url:
            return HttpResponseNotFound("Resource not found or expired")

        # Prepare headers for Range support
        headers = {}
        range_header = request.headers.get('Range')
        if range_header:
            headers['Range'] = range_header

        # Use requests to fetch the content from MinIO with the presigned URL
        session = requests.Session()
        req = requests.Request('GET', presigned_url, headers=headers)
        prepped = session.prepare_request(req)

        # Remove any Authorization header to avoid multi-auth error
        prepped.headers.pop('Authorization', None)

        resp = session.send(prepped, stream=True)
        if resp.status_code not in [200, 206]:
            return HttpResponseNotFound("File not found or expired")

        django_response = StreamingHttpResponse(resp.iter_content(chunk_size=8192), status=resp.status_code)
        django_response['Content-Type'] = resp.headers.get('Content-Type', 'application/octet-stream')
        django_response['Content-Length'] = resp.headers.get('Content-Length', '')
        if 'Content-Range' in resp.headers:
            django_response['Content-Range'] = resp.headers['Content-Range']
        django_response['Accept-Ranges'] = 'bytes'

        # Optional: suggest filename for download
        django_response['Content-Disposition'] = f'attachment; filename="{resource.title}"'

        return django_response
