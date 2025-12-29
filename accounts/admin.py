from django.contrib import admin
from .models import Profile
from core.admin_actions import export_as_xlsx  # Импортируй

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'birth_date')
    search_fields = ('user__username', 'phone_number')
    actions = [export_as_xlsx]  # Добавь действие