from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import home, login, add_employee, user_profile, user_settings

app_name = "base"
urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('add_employee/', add_employee, name='add_employee'),
    path('user_profile/', user_profile, name='user_profile'),
    path('user_settings/', user_settings, name='user_settings')
]

if settings.DEBUG: 
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
