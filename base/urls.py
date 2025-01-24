from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import home, login, add_employee

app_name = "base"
urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('add_employee/', add_employee, name='add_employee')
]

if settings.DEBUG: 
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
