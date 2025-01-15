from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import include, path
from quiz_app.views import CustomUserViewSet
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz_app.urls')),
    path('info/', include(router.urls)), 
     path('info/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]