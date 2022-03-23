from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('',views.welcome, name='welcome'),
    path('home/',views.home, name='demo-home'),
    path('about/',views.about, name='demo-about'),
    # path('devotee/',views.devoteeList, name='devotee-about'),
    path('wg/',views.wg, name='demo-wg'),
    path('wg-exception/',views.callweekgenexception, name='Weekgen-exception'),
    path('generatewhatsapp',views.generatewhatsapp, name = 'demo= whatz'),
    path('register/',views.checkregistrationdetails, name='Register'),
    path('login/',views.login_request, name='Login'),
    path('logout/',views.logoutUser, name='Logout'),
    path('volunteerlist/',views.volunteerlist, name='volunteerlist'),
    path('volunteerlist/<int:volunteerid>',views.volunteerdetails, name='volunteerdetails'),
    path('volunteerlist/volunteeradd/',views.volunteeradd, name='volunteeradd'),
    path('volunteertodevotee/<int:volunteerid>',views.volunteertodevotee, name='volunteertodevotee'),
    # path('weekgen/',views.callweekgen, name='weekly-Gen'),
    url(r'external',views.external),
    url(r'callweekgen',views.callweekgen),
    url(r'callweekgenexception',views.callweekgenexception),
    url(r'form',views.Form),
    url(r'upload',views.upload),
    url(r'generatewhatsapp',views.generatewhatsapp),
]

