from django.db import models

# Create your models here.
class userModel(models.Model):
    username = models.CharField(max_length=30)
    contact = models.CharField(max_length=10 , default='Null')
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=15)
    cpassword = models.CharField(max_length=15)

class photos(models.Model):
    image = models.ImageField(upload_to='upload/photos/')

    @staticmethod
    def get_all_products():
        return photos.objects.all()

class faqsQA(models.Model):
    question = models.CharField(max_length=50)
    answer = models.CharField(max_length=200)

    @staticmethod
    def get_all_products():
        return faqsQA.objects.all()
    
class testimonial(models.Model):
    feedback = models.CharField(max_length=300)
    username = models.CharField(max_length=30)
    ename = models.CharField(max_length=20)

    @staticmethod
    def get_all_products():
        return testimonial.objects.all()
    
class eventPage(models.Model):
    eventName = models.CharField(max_length=30)
    Description = models.CharField(max_length=200)

    @staticmethod
    def get_all_products():
        return eventPage.objects.all()
    
class quiry(models.Model):
    uname = models.CharField(max_length=30)
    umail = models.EmailField(max_length=30)
    uquery = models.CharField(max_length=200)

class Package(models.Model):
    event = models.ForeignKey(eventPage, on_delete=models.CASCADE)
    packageName = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Booking(models.Model):
    user = models.ForeignKey(userModel, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    package_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    address = models.TextField(null=True, blank=True)
    event_date = models.DateField(null=True, blank=True)
    event_time = models.TimeField(null=True, blank=True)

    @property
    def event_name(self):
        return self.package.event.eventName

    def nameofuser(self):
        return self.user.username

    def __str__(self):
        return f"{self.user.username} - {self.package_name}"