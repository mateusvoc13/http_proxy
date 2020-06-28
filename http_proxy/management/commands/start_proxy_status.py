from django.core.management.base import BaseCommand
from http_proxy.models import ProxyStatus


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not ProxyStatus.objects.filter(id=1):
            ProxyStatus.objects.create(id=1).save()
