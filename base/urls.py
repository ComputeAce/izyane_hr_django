from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import home, login, user_profile, user_settings, view_employee, logout_user

app_name = "base"
urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
 
    path('user_profile/', user_profile, name='user_profile'),
    path('user_settings/', user_settings, name='user_settings'),
    path('employee/', view_employee, name='view_employee'),
    path('logout_user/', logout_user, name='logout_user'),

    
]

if settings.DEBUG: 
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
