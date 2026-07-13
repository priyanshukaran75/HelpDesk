from django.contrib import admin
from .models import Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','department','designation','phone']
    search_fields = ['user__username','user__first_name','user__last_name','department']
    list_filter = ['department']
    raw_id_fields = ['user']
# Register your models here.
