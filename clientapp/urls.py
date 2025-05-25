from django.urls import path
from .views import LeadCreateView, LeadListView, LeadDetailView, LeadUpdateView, LeadResumeView
from django.conf.urls.static import  static
from django.conf import settings



urlpatterns = [
    path('api/leads/', LeadCreateView.as_view(), name='lead-create'),
    path('api/leads/list/', LeadListView.as_view(), name='lead-list'),
    path('api/leads/<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('api/leads/<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),

    #admin panel orqali resumini ko'rishni bosganda
    path('api/leads/<int:pk>/resume/', LeadResumeView.as_view(), name='lead-resume'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)