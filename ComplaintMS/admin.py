from django.contrib import admin
from .models import Profile,Complaint,Grievance

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'collegename', 'contactnumber', 'type_user', 'Branch')
    list_filter = ('type_user', 'collegename', 'Branch')
    search_fields = ('user__username', 'user__email', 'contactnumber')

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('Subject', 'user', 'Type_of_complaint', 'priority', 'status', 'Time')
    list_filter = ('status', 'Type_of_complaint', 'priority', 'Time')
    search_fields = ('Subject', 'Description', 'user__username')
    readonly_fields = ('ai_analysis',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('Subject', 'user', 'Type_of_complaint', 'Description')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority')
        }),
        ('AI Analysis', {
            'fields': ('ai_analysis',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        # Add priority with color coding
        return list_display

@admin.register(Grievance)
class GrievanceAdmin(admin.ModelAdmin):
    list_display = ('guser',)
    search_fields = ('guser__username', 'guser__email')

# Custom admin site configuration
admin.site.site_header = "Complaint Management System Admin"
admin.site.site_title = "CMS Admin Portal"
admin.site.index_title = "Welcome to Complaint Management System"
