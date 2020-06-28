from django.http import HttpResponse

from django.views import View
from django.views.generic import DetailView

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from http_proxy.models import ProxyStatus
from http_proxy.controller import update_proxy_status
from http_proxy.request_factory import generate_request


@method_decorator(csrf_exempt, name='dispatch')
class ProxyView(View):

    def post(self, request, *args, **kwargs):
        """
        This function aims to process the requests that are going through the Proxy

        For now, syncrounoulsy, it is creating requests to the main server.
        """
        update_proxy_status()
        return HttpResponse(generate_request(request))


class StatusPage(DetailView):
    model = ProxyStatus
    template_name = 'status.html'

    def get_object(self):
        return ProxyStatus.objects.order_by('id').first()
