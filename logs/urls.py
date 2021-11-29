from django.urls import path, re_path

from .views import EchoView

urlpatterns = [
    re_path(r'^logs?$', EchoView.as_view()),
]
