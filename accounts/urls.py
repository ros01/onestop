from . import views
from django.urls import path
from .views import (
    LoginTemplateView, SignUpView,  
)



app_name = 'accounts'




urlpatterns = [
    path('portal_account_creation/', SignUpView.as_view(), name='create_portal_account'),
    path('signin', LoginTemplateView.as_view(), name='signin'),
    path('login', views.login, name='login'), 
    path('logout', views.logout, name='logout'),
  
     

]

