from django.contrib import admin
from .models import ContactSubmission, CompetitionApplication, PortfolioHolding

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

@admin.register(PortfolioHolding)
class PortfolioHoldingAdmin(admin.ModelAdmin):
    list_display = ("ticker", "shares", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("ticker",)
    readonly_fields = ("created_at", "updated_at")
    
    fieldsets = (
        ('Holding Information', {
            'fields': ('ticker', 'shares', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Make the list editable for quick updates
    list_editable = ('shares', 'is_active')
    
    # Add action to bulk activate/deactivate
    actions = ['activate_holdings', 'deactivate_holdings', 'clear_cache']
    
    def activate_holdings(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} holdings activated.')
    activate_holdings.short_description = "Activate selected holdings"
    
    def deactivate_holdings(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} holdings deactivated.')
    deactivate_holdings.short_description = "Deactivate selected holdings"

    def clear_cache(self, request, queryset):
          from .services import PortfolioService
          service = PortfolioService()
          service.clear_cache()
          self.message_user(request, 'Cache cleared!')
    clear_cache.short_description = "Clear portfolio cache"