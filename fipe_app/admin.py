from django.contrib import admin
from django.utils.formats import number_format
from .models import Lead

class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'phone', 'brand', 'model', 'year', 'fuel', 'formatted_price', 
        'market_category', 'car_category', 'formatted_original_price', 
        'formatted_pricing_percentage', 'under_warranty', 'revisions_done_in_css', 'created_at'
    )
    
    search_fields = ('name', 'email', 'phone', 'brand', 'model', 'year')
    
    list_filter = ('brand', 'model', 'year', 'fuel', 'market_category', 'car_category', 'under_warranty', 'revisions_done_in_css')

    ordering = ('-created_at',)
    
    list_editable = ('under_warranty', 'revisions_done_in_css')

    list_display_links = ('name', 'email', 'phone')

    def formatted_pricing_percentage(self, obj):
        percentage = obj.pricing_percentage
        if percentage is not None:
            return f"{percentage * 100}%"
        return ""

    formatted_pricing_percentage.short_description = "Pricing Percentage"
    
    def formatted_price(self, obj):
        if obj.price is not None:
            return f"R$ {number_format(obj.price, 2, force_grouping=True, use_l10n=True)}"
        return ""

    formatted_price.short_description = "Price"

    def formatted_original_price(self, obj):
        if obj.original_price is not None:
            return f"R$ {number_format(obj.original_price, 2, force_grouping=True, use_l10n=True)}"
        return ""

    formatted_original_price.short_description = "Original Price"

admin.site.register(Lead, LeadAdmin)

