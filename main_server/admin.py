from django.contrib import admin
from main_server.models import DecodedJWT
# Register your models here.


class DecodedJWTAdmin(admin.ModelAdmin):
    fields = ['iat', 'jti', 'payload']


admin.site.register(DecodedJWT, DecodedJWTAdmin)
