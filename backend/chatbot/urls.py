# your_app_name/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, FAQViewSet, StaffViewSet, RequestorViewSet, PDFUploadView, UserViewSet
from .authentication import urlpatterns as auth_urls

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'requestors', RequestorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload_pdf/', PDFUploadView.as_view({'post': 'create'})),
    path('auth/', include(auth_urls)),
    path('register/', UserViewSet.as_view({'post': 'register'}), name='register'),
]
