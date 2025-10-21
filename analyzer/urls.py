from django.urls import path, re_path
from .views import StringView

urlpatterns = [
    path("strings/", StringView.as_view(), name="string-list-create"),
    re_path(r"^strings/(?P<string_value>.+)/$", StringView.as_view(), name="string-detail"),
]
