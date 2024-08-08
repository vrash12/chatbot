# views.py
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.conf import settings
from .models import Message, FAQ, Staff, Requestor
from .serializers import MessageSerializer, FAQSerializer, StaffSerializer, RequestorSerializer, UserSerializer
from .chatbot import Chatbot
from .utils.pdf_extractor import extract_text_from_pdf
import os

chatbot = Chatbot()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role')  # Role can be 'staff' or 'requestor'

        user = User.objects.create_user(username=username, password=password)
        
        if role == 'staff':
            Staff.objects.create(name=username, email=user.email)  # You might want to customize these fields
        else:
            Requestor.objects.create(name=username, email=user.email)  # You might want to customize these fields

        return Response({'status': 'User registered'}, status=status.HTTP_201_CREATED)

        

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_input = request.data.get('text')
        user = request.user
        
        # Get chatbot response
        response_text = chatbot.get_response(user_input)

        # Save the user message and encrypted response
        message = Message.objects.create(user=user, text=user_input)
        message.encrypt_response(response_text)

        # Return the encrypted response
        return Response({'response': message.encrypted_response}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def history(self, request):
        user = request.user
        messages = Message.objects.filter(user=user).order_by('-timestamp')
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

class PDFUploadView(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        file_obj = request.data['file']
        file_path = os.path.join(settings.MEDIA_ROOT, file_obj.name)
        
        with open(file_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
        
        # Extract text from the PDF
        pdf_text = extract_text_from_pdf(file_path)
        
        # Update chatbot context
        chatbot.update_context(pdf_text)
        
        return Response({'status': 'PDF processed and context updated'}, status=status.HTTP_201_CREATED)

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class RequestorViewSet(viewsets.ModelViewSet):
    queryset = Requestor.objects.all()
    serializer_class = RequestorSerializer

