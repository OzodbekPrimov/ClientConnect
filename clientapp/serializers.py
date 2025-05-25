from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lead
        fields = ['first_name', 'last_name', 'email', 'resume', 'state']

    resume = serializers.FileField()

# holatni yangilashda faqat state ni kiritadi
class LeadUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['state']

    def validate(self, data):
        # Faqat state maydonini tekshiramiz
        if 'state' not in data and any(key not in ['state'] for key in data.keys()):
            raise serializers.ValidationError("Only 'state' field can be updated.")
        return data

