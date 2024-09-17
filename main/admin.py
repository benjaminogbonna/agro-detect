from django.contrib import admin
from .models import DiseaseDetection

@admin.register(DiseaseDetection)
class DiseaseDetectionAdmin(admin.ModelAdmin):
    ordering = ('-detected_at',)
    list_display = ['prediction', 'prob', 'detected_at']
    search_fields = ['prediction']
    list_filter = ['prediction']
