from django.contrib import admin
from django.urls import path
from http_proxy.views import ProxyView, StatusPage
from main_server.views import MainServer

urlpatterns = [
    path('', StatusPage.as_view(), name='proxy-status-page'),
    path('admin/', admin.site.urls),
    path('proxy/', ProxyView.as_view(), name='proxy-view'),
    path('server/', MainServer.as_view(), name='main-server-view'),
]
