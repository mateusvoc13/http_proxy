from django.contrib import admin
from http_proxy.models import ProxyStatus


class ProxyStatusAdmin(admin.ModelAdmin):
    readonly_fields = ['start_time', 'request_count']


admin.site.register(ProxyStatus, ProxyStatusAdmin)
