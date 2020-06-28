from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from main_server.controller import store_jwt


@method_decorator(csrf_exempt, name='dispatch')
class MainServer(View):

    def post(self, request, *args, **kwargs):
        """
        In order to validate the JWT requests, the three claims will be stored in a Mock "DecodedJWT" model.
        """

        if store_jwt(request.headers):
            return HttpResponse('JWT Stored')

        return HttpResponse("Error while trying to Parse the JWT")
