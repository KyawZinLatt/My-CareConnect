from django.urls import path
from . import views
from rest_framework import routers
from django.conf.urls import include
from callcenter.views import CaseListView, ClientNewPhView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView

#app_name = 'callcenter'


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'client-phones', views.ClientPhoneViewSet)
router.register(r'client-symptom-question-answer-list', views.ClientSymptomQuestionAnswerViewSet)
router.register(r'chatbotclient', views.ChatbotClientViewSet)




urlpatterns = [
    path('', login_required(views.index), name='index'),
    path('clients/<int:id>/additional-ph', views.add_additional_ph, name='client_additional_phone'),
    path('clients/<int:id>/info/', views.first_contact, name='client_info'),
    path('clients/<int:id>/symptoms/', views.symptoms_confirmed_by_call, name='client_call_symptoms'),
    path('clients/<int:id>/refer/', views.refer_tb_client, name='refer_tb_client'),
    path('clients/<int:id>/social-platforms/', views.is_active_in_social_platforms, name='client_active_social_platforms'),
    path('state_regions/', views.get_state_regions),
    path('townships/<int:state_region_id>/', views.get_townships, name='get_townships'),
    path('channels/<int:township_id>/', views.get_channels, name='channels'),
    path('site_addresses/<int:state_region_id>/<int:township_id>/<int:channel_id>/', views.get_site_addresses, name='site_addresses'),
    path('clients/<int:id>/refer-locations/', views.refer_locations, name='client_ref_locations'),
    path('clients/<int:id>/reach-info/', views.reach_info, name='client_reach_info'),
    path('investigation_types/', views.get_investigation_types),
    path('investigation_results/<int:investigation_type_id>/', views.get_investigation_results),
    path('clients/<int:id>/taken-investigations/', views.taken_investigations, name='client_taken_investigations'),
    path('clients/<int:id>/tb-confirmation/', views.tb_confirmation, name='client_tb_confirmation'),
    path('tb_regimes/', views.get_tb_regimes),
    path('clients/<int:id>/tb-treatment/', views.tb_treatment, name='client_tb_treatment'),
    path('investigation-results', views.load_investigation_results, name='investigation_results'),
    path('townships/', views.load_townships, name='townships'),
    path('addresses/', views.load_addresses, name='addresses'),
    path('clinic/', views.load_clinic, name='clinic'),

    # path('channel/', views.load_channel, name='channel'),
    # path('organization/', views.load_organization, name='organization'),
    #path('sites/', views.load_available_sites, name='sites'),
    #path('test/', views.test, name='test'),
    path('testone/', views.testone, name='test'),
    path('create-client/', views.create_client, name='create-client'),
    path('test-co-pilot/', views.test_co_pilot, name='test-co-pilot'),
    path('new-tb-referral/', views.new_tb_referral, name='new-tb-referral'),
    path('test-api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('cases/', CaseListView.as_view(), name='case_list'),
    # path('login/', LoginView.as_view(), name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('clients/<int:id>/', login_required(views.client_details), name='client_details'),
    path('clients/<int:pk>/new-contact', views.client_stage1_new_contact, name='client_stage1_new_contact'),
    path('clients/<int:pk>/additional-contact', views.client_stage1_additional_contact, name='client_stage1_additional_contact'),
    path('clients/<int:pk>/new-ph', ClientNewPhView.as_view(), name='client_new_ph'),
    path('clients/<int:pk>/new-diagnosis', views.client_stage2_new_diagnosis, name='client_stage2_new_diagnosis'),
    path('clients/<int:pk>/new-investigation', views.client_stage2_new_investigation, name='client_stage2_new_investigation'),
    path('clients/<int:pk>/new-tb-register', views.client_stage3_new_tb_register, name='client_stage3_new_tb_register'),
    #path('test-api/client-question-answer-bulk-create-update/', views.ClientSymptomQuestionAnswerView.as_view(), name='client-question-answer-bulk-create-update'),
    #path('use-coupon/', views.UseCouponView.as_view(), name='coupon')
    #?coupon_code=COUPONTEST01
]