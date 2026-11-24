from django.contrib import admin
from .models import Request,Service,Review,Chat,Ticket
@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display=('id','name','service','status','created')
    list_filter=('status','service','priority')
    search_fields=('name','phone','title')
    readonly_fields=('code','created')
admin.site.register([Service,Review,Chat,Ticket])
admin.site.site_header='IT Support Pro • Управление'
