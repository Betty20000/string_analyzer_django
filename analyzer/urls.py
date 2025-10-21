from django.urls import path, re_path
from analyzer.views import StringView

urlpatterns = [
    # Handles both with and without trailing slash
    re_path(r"^strings/?$", StringView.as_view(), name="strings"),
    re_path(r"^strings/(?P<string_value>[^/]+)/?$", StringView.as_view(), name="string_detail"),
]
