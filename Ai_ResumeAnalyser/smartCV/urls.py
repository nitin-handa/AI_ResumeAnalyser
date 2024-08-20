from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from smartCV_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('upload', views.uploadResume, name='upload'),
    path('save_skills', views.saveSkills, name='saveskills'),
    path('fetch_data', views.fetchData, name='fetch'),
    path('fetch_auth_page', views.fetch_auth_page, name='fetch_auth_page'),
    path('up_data', views.up_data, name='up_data'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)