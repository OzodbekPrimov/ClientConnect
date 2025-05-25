from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Lead
from rest_framework import status
import os


class LeadAPITestCase(APITestCase):
    def setUp(self):
        # test uchun  user yaratamiz
        self.user = User.objects.create_user(username="Ozodbek", password="testparol")
        self.client = APIClient()
        self.client.login(username="Ozodbek", password="testparol")

        self.lead_data = {
            'first_name': 'Ozod',
            'last_name': 'Primov',
            'email': 'primovozodbek5@gmail.com',
            'resume': SimpleUploadedFile('resume.pdf', b'Test resume', content_type='application/pdf'),
        }

        self.lead = Lead.objects.create(
            first_name = 'Jamol',
            last_name='Kamolov',
            email='primovo67@gmail.com',
            resume=SimpleUploadedFile('test_resume.pdf', b'Test pdf', content_type='application/pdf')
        )

    def test_create_lead(self):
        url = reverse('lead-create')
        response = self.client.post(url, self.lead_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lead.objects.count(), 2)

    def test_list_leads_authentication(self):
        url = reverse('lead-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'Jamol')

    def test_list_lead_unauthenticated(self):
        self.client.logout()
        url = reverse('lead-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_lead_authenticated(self):
        url = reverse('lead-detail', kwargs={'pk':self.lead.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lead_state(self):
        url = reverse('lead-update', kwargs={'pk': self.lead.pk})
        update_data = {'state':'REACHED_OUT'}
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        """Testdan keyin fayllarni tozalash"""
        for lead in Lead.objects.all():
            if lead.resume:
                if os.path.exists(lead.resume.path):
                    os.remove(lead.resume.path)
