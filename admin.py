from django.contrib import admin
from .models import userModel,photos,faqsQA,testimonial,eventPage,quiry,Package,Booking

from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from .models import Booking


# Register your models here.
class Admincustomer(admin.ModelAdmin):
    list_display = ['username','contact','email','password','cpassword']

class Admingallary(admin.ModelAdmin):
    list_display = ['image']

class Adminfaqs(admin.ModelAdmin):
    list_display = ['question','answer']

class AdminFB(admin.ModelAdmin):
    list_display = ['feedback','username','ename']

class AdminEpage(admin.ModelAdmin):
    list_display = ['eventName','Description']

class AdminQuery(admin.ModelAdmin):
    list_display = ['uname','umail','uquery']

class AdminPack(admin.ModelAdmin):
    list_display = ['event','packageName','description','price']

class AdminBooking(admin.ModelAdmin):
    list_display = ['user', 'package', 'package_name', 'price', 'booking_date', 'address', 'event_date', 'event_time']

    def report_buttons(self, request):
        return format_html(
            '<a href="{}" class="button">Weekly Report</a> '
            '<a href="{}" class="button">Monthly Report</a> '
            '<a href="{}" class="button">Yearly Report</a>',
            reverse('generate_report', args=['weekly']),
            reverse('generate_report', args=['monthly']),
            reverse('generate_report', args=['yearly'])
        )
    
    report_buttons.allow_tags = True
    report_buttons.short_description = "Generate Reports"

admin.site.register(userModel , Admincustomer)
admin.site.register(photos , Admingallary)
admin.site.register(faqsQA , Adminfaqs)
admin.site.register(testimonial , AdminFB)
admin.site.register(eventPage , AdminEpage)
admin.site.register(quiry , AdminQuery)
admin.site.register(Package , AdminPack)
admin.site.register(Booking, AdminBooking)