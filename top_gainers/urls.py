from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("refresh", views.refresh_data, name="refresh"),
    path("detail/", views.get_stock_detail, name='detail')
]
