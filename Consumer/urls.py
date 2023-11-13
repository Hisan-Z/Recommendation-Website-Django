from django.urls import include, path

from . import views

urlpatterns = [
    path('signup/', views.signupuser,name="signup"),
    path('login/',views.loginuser,name="login"),
    path('logout/',views.logoutuser,name="logout"),
    path('accounts/social/login/cancelled/',views.redirecthome),
    path('accounts/',include('allauth.urls'), name='uauth'),  
    path('changepassword',views.changepassword,name="changepass"),
]