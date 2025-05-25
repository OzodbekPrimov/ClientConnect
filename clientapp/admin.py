# leads/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Lead
from django.urls import reverse

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'state', 'created_at', 'resume_link')  # resume_link qo‘shildi
    list_filter = ('state', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    readonly_fields = ('created_at',)

    def resume_link(self, obj):
        if obj.resume:
            # Havolani API endpoint’iga yo‘naltirish
            url = reverse('lead-resume', kwargs={'pk': obj.pk})  # lead-resume nomli URL
            return format_html('<a href="{}" target="_blank">View Resume</a>', url)
        return "No Resume"
    resume_link.short_description = 'Resume'