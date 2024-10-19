from django.urls import path,re_path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    re_path('login/',views.login),
    re_path('Register/',views.Register),
    re_path('profile/',views.profile),
    re_path('updateProfile/',views.update_profile),
    

]