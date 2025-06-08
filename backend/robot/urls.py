from django.urls import path
from .views import home_view, draw_page, run_draw

urlpatterns = [
    path("", home_view, name="home"),
    path("draw/<int:pk>/", draw_page, name="draw_page"),
    path("draw/<int:pk>/run/", run_draw, name="run_draw"),
]
