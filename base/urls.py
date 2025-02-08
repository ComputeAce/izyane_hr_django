from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import home, login, user_profile, view_employee, logout_user, update_profile_img,  update_password, submit_change_password, forget_password

app_name = "base"
urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('update_profile_img/', update_profile_img, name='update_profile_img'),
    path('user_profile/', user_profile, name='user_profile'),
    path('employee/', view_employee, name='view_employee'),
    path('logout_user/', logout_user, name='logout_user'),
    path('update_password/',  update_password, name=' update_password'),
    path('submit_change_password/', submit_change_password, name='submit_change_password'),
    path('forget_password/', forget_password, name='forget_password')

    
]

if settings.DEBUG: 
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)