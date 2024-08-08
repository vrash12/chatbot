from django.contrib import admin
from .models import Message, FAQ, Staff, Requestor

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'timestamp', 'status', 'addressed_by')
    list_filter = ('status', 'timestamp')
    search_fields = ('user', 'text', 'intent')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
    search_fields = ('question', 'answer')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'position', 'available')
    list_filter = ('available',)
    search_fields = ('name', 'email', 'position')

@admin.register(Requestor)
class RequestorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'student_id')
    search_fields = ('name', 'email', 'student_id')
