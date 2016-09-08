import rest_framework_jwt.views
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r'clients', views.ClientsViewSet, base_name='clients')
router.register(r'networks', views.NetworksViewSet, base_name='networks')
router.register(r'daemons', views.DaemonsViewSet, base_name='daemons')
router.register(r'users/me', views.UserMeViewSet, base_name='me')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^tokens/auth/', rest_framework_jwt.views.obtain_jwt_token),
    url(r'^tokens/verify/', rest_framework_jwt.views.verify_jwt_token),
    url(r'^tokens/refresh/', rest_framework_jwt.views.refresh_jwt_token),
    url(r'^auth/', include('djoser.urls')),
]
