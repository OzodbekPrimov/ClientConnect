from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Lead
from .serializers import LeadSerializer
from django.core.mail import send_mail
from drf_yasg import openapi



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
                'state': openapi.Schema(type=openapi.TYPE_STRING, enum=['PENDING', 'REACHED_OUT']),
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
            # Adminga xabar
            send_mail(
                subject='Yangi Mijoz',
                message=f'Yangi mijoz {lead.first_name} {lead.last_name} forma yubordi. Email: {lead.email}',
                from_email='oprimov13@gmail.com',
                recipient_list=['primovozodbek5@gmail.com'],  # Admin/advokat emaili
                fail_silently=False,
            )
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
    def patch(self, request, pk):
        lead = Lead.objects.get(pk=pk)
        serializer = LeadSerializer(lead, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
