from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import generate_report

urlpatterns = [
    path('', views.Home),
    path('Home',views.Home, name='Home'),
    path('Event.html', views.Event, name='Event'),
    path('About_Us.html', views.about_us, name='AboutUs'),
    path('Contact_Us.html', views.contactUs, name='ContactUs'),
    path('FAQs_Page.html', views.faqs, name='FAQs'),
    path('Gallary_Page.html', views.gallary, name='Gallary'),
    path('Login_Page.html', views.login, name='LogIn'),
    path('regi.html', views.registration, name='registration'),
    path('EV_CA.html/<int:event_id>/',views.package, name='package'),
    path('logout/', views.logout_view, name='logout'),
    path('confirm_booking/', views.confirm_booking, name='confirm_booking'),
    path('generate_report/<str:report_type>/', generate_report, name='generate_report')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
