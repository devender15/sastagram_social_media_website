from django.urls import path
from users.views import (
            login_view,
            logout_view,
            account_view,
            registration_view,
        )
        
urlpatterns  = [
    path('register/',registration_view, name="register" ),
    path('logout/',logout_view, name="logout" ),
    path('login/',login_view, name="login" ),
]