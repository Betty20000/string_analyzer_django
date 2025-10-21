from django.urls import path
from .views import StringView

urlpatterns = [
    # Create new string OR list/filter/natural query
    path("strings/", StringView.as_view(), name="string-list-create"),

    # Fetch or delete a specific string by its raw value
    path("strings/<str:string_value>/", StringView.as_view(), name="string-detail"),
]
