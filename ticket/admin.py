from django.contrib import admin
from .models import Ticket,TicketComment
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number','title','category','priority','status','created']
    list_filter = ['status','priority','category','created']
    search_fields = ['title','description']
    ordering = ['-created']
@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ["ticket", "user", "created"]
# Register your models here.
