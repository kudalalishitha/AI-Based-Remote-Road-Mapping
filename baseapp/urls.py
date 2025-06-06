from baseapp import views as views
from django.urls import path


urlpatterns = [
 
    path('about/',views.about,name="about"),
    path('admin/login',views.admin_login,name="admin_login"),
    path('login/',views.user_login,name="user_login"),
    path('register/',views.user_register,name="user_register"),
    path('contact/',views.contact,name="contact"),
    path('otp/',views.user_otp,name="user_otp"),
    
    
]