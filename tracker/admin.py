from django.contrib import admin
from .models import ContactSubmission, CompetitionApplication

# Register your models here.

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("full_name", "au_email", "submitted_at")
    search_fields = ("full_name", "au_email")
    readonly_fields = ("submitted_at",)

@admin.register(CompetitionApplication)
class CompetitionApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "competition_type", "submitted_at")
    list_filter = ("competition_type",)
    search_fields = ("full_name", "email")
    readonly_fields = ("submitted_at",)