"""registration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app1 import views
from django.conf.urls import handler404
from app1.views import signup_view
from rest_framework.routers import DefaultRouter
from app1.views import EventViewSet, TeamViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'teams', TeamViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='index_view'),
    path('login/', views.login_view, name='login_view'),
    path('whoru/', views.whoru, name='whoru'),
    path('voter_login.html', views.voter_login, name='voter_login'),
    path('official_signup/', views.official_signup_view, name='official_signup_view'),
    path('login/verify-otp1/', views.verify_otp1_view, name='verify-otp1'),
    path('login/verify-otp2/', views.verify_otp2_view, name='verify-otp2'),
    path('official_login.html', views.official_login, name='official_login'),
    path('official_dashboard/', views.official_dashboard, name='official_dashboard'),
    path('official_login/verify-otp3/', views.verify_otp3_view, name='verify-otp3'),
    path('validate-aadhar/<int:aadhar_number>/', views.validate_aadhar, name='validate_aadhar'),
    path('validate-login/<str:aadhar_number>/<str:password>/', views.validate_login, name='validate_login'),
    path('home/', views.home_view, name='home'),
    path('homes/', views.homes_view, name='homes'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', signup_view, name='signup_view'),
    path('add_event/', views.add_event, name='add_event'),
    path('api/events/', views.get_events, name='api-events'),
    path('api/event_details/<str:event_name>/', views.event_details, name='event_details'),
    path('api/events/', views.event_list, name='event-list'),
    path('fetch_upcoming_events', views.fetch_upcoming_events, name='fetch_upcoming_events'),
    path('fetch_event_details/', views.fetch_event_details, name='fetch_event_details'),
    path('send-notification/', views.send_notification, name='send_notification'),
    path('save-vote/', views.save_vote, name='save_vote'),
    path('download_cert/', views.download_cert, name='download_cert'),
    path('download_certificate/', views.download_certificate, name='download_certificate'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('send_otp/', views.send_otp, name='send_otp'),
    path('verify-vote/', views.verify_vote, name='verify_vote'),
    path('verify/', views.verify_votes, name='verify_votes'),
    path('verify_certificate/', views.render_verify_certificate, name='verify_certificate'),
    path('', include(router.urls)),
]

handler404 = views.error_404