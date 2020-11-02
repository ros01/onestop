from django.urls import path
from . import views
from .views import (
    HomepageTemplateView,
    



)

urlpatterns = [
    #path('', views.index, name='index'),
    path('', HomepageTemplateView.as_view(), name='index'),
    
    
    ]