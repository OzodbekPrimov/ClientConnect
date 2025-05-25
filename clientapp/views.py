from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Lead
from .serializers import LeadSerializer, LeadUpdateSerializer
from django.core.mail import send_mail
from drf_yasg import openapi
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import os
from django.http import FileResponse


class LeadCreateView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Create a new lead",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
                'resume': openapi.Schema(type=openapi.TYPE_FILE),  # Fayl maydoni
            },
            required=['first_name', 'last_name', 'email', 'resume']
        ),
        responses={201: LeadSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = LeadSerializer(data=request.data)
        if serializer.is_valid():
            lead = serializer.save()
            # Mijozga tasdiqlovchi email
            send_mail(
                subject='Ariza qabul qilindi',
                message=f'Hurmatli {lead.first_name}, sizning arizangiz muvaffaqiyatli qabul qilindi. Tez orada siz bilan bog‘lanamiz.',
                from_email='oprimov13@gmail.com',
                recipient_list=[lead.email],
                fail_silently=False,
            )
            # Adminga xabar bilan resume faylini biriktirish
            admin_email = EmailMultiAlternatives(
                subject='New Client',
                body=f'New client {lead.first_name} {lead.last_name} submitted a form. Email: {lead.email}',
                from_email=settings.EMAIL_HOST_USER,
                to=['primovozodbek5@gmail.com'],  # Admin emaili
            )
            # Resume faylini biriktirish
            resume_path = lead.resume.path  # Faylning serverdagi yo'li
            if os.path.exists(resume_path):
                admin_email.attach_file(resume_path)  # Faylni biriktirish
            else:
                admin_email.body += "\n\nNote: Resume file could not be attached due to an error."
            admin_email.send(fail_silently=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LeadListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        leads = Lead.objects.all()
        serializer = LeadSerializer(leads, many=True)
        return Response(serializer.data)

class LeadDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        lead = Lead.objects.get(pk=pk)
        serializer = LeadSerializer(lead)
        return Response(serializer.data)

class LeadUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update the state of a lead",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'state': openapi.Schema(type=openapi.TYPE_STRING, enum=['PENDING', 'REACHED_OUT']),
            },
            required=['state']
        ),
        responses={200: LeadUpdateSerializer, 400: "Bad Request", 404: "Lead not found"}
    )
    def patch(self, request, pk):
        lead = Lead.objects.get(pk=pk)
        serializer = LeadSerializer(lead, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeadResumeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            lead = Lead.objects.get(pk=pk)
            if lead.resume:
                return FileResponse(lead.resume.open('rb'), as_attachment=True, filename=lead.resume.name)
            return Response({"error": "No resume found for this lead"}, status=status.HTTP_404_NOT_FOUND)
        except Lead.DoesNotExist:
            return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)
