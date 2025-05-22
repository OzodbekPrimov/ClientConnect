from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    resume = serializers.FileField()

    class Meta:
        model = Lead
        fields = ['first_name', 'last_name', 'email', 'resume', 'state']
