from django.contrib import admin
from .models import Membership, Order
from .admin_actions import export_as_xlsx  # Импортируй действие

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    actions = [export_as_xlsx]  # Добавь действие

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'membership', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'membership__name')
    actions = [export_as_xlsx]  # Добавь действие
