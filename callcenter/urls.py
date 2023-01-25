from django.urls import path
from . import views
from rest_framework import routers
from django.conf.urls import include

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('testone/', views.testone, name='test'),
    path('create-client/', views.create_client, name='create-client'),
    path('test-co-pilot/', views.test_co_pilot, name='test-co-pilot'),
    path('new-tb-referral/', views.new_tb_referral, name='new-tb-referral'),
    path('test-api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]