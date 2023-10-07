from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signupuser,name="signup"),
    path('login/',views.loginuser,name="login"),
    path('logout/',views.logoutuser,name="logout"),
    path('changepassword',views.changepassword,name="changepass"),
]