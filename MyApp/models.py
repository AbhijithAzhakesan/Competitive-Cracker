from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.urls import reverse

# Create your models here.
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_course = models.BooleanField(default=False)
    is_video=models.BooleanField(default=False)
    is_materials=models.BooleanField(default=False)

class Customers(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key=True, related_name='Customer')
    First_Name = models.CharField(max_length = 20)
    Last_Name = models.CharField(max_length = 20)
    State = models.CharField(max_length = 20)
    District = models.CharField(max_length = 20)
    Email = models.EmailField(max_length = 30)
    Phone_Number = models.IntegerField()
    image=models.ImageField(upload_to='StudentImage')
    
    def __str__(self):
        return self.First_Name

class TeachersLogin(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key =True, related_name='TeachersLogin')
    Name=models.CharField(max_length=20)
    Subject=models.CharField(max_length=20)
    Email= models.EmailField()
    Phone_Number=models.IntegerField()
    image=models.ImageField(upload_to='TeacherImage')
    
    def __str__(self):
        return self.Name

class Courses(models.Model):
    course_name= models.CharField(max_length=20)
    course_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)
    image = models.ImageField(upload_to='CourseImages')
    
    def __str__(self):
        return self.course_name
    
    def get_purchase_url(self):
        return reverse('buy_now', args=[self.pk])

class OnlineClass(models.Model):
    title = models.CharField(max_length=100)
    description= models.TextField()
    date_time= models.DateField()
    class_hours= models.IntegerField()
    instructor = models.CharField(max_length=20)
    video = models.FileField(upload_to='videos')
    
    def __str__(self):
        return self.title
    
class StudyMaterials(models.Model):
    title=models.CharField(max_length=30)
    topic= models.CharField(max_length=30)
    date=models.DateField()
    pdf_notes=models.FileField(upload_to='study_materials')
    
    def __str__(self):
        return self.title

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} purchased {self.course.title} on {self.purchase_date}'

class Cart_courses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s Cart - {self.course.course_name}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"