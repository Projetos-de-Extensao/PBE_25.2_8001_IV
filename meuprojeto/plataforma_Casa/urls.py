from django.urls import path
from .views import sql_view

urlpatterns = [
    path('sql/', sql_view, name='sql_view'),
    ]