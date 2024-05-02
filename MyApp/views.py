from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from MyApp.forms import CourseReg, Materials, TeachersReg, User_register, Video, signup
from MyApp.models import Cart_courses, Courses, Customers, StudyMaterials, TeachersLogin, OnlineClass, Purchase, Order

# Create your views here.
def HomePage(request):
    return render(request,'index.html')

def careers(request):
    return render(request, 'Carrers.html')

def contactus(request):
    return render(request, 'Contactus.html')
            
def loginPage(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password =  request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect (AdminPage)
            elif user.is_customer:
                return redirect(MyProfile)
            elif user.is_teacher:
                return redirect(TeachersPage)
        else:
            messages.info(request, message='Not a Registered User')
    return render(request,'login.html')

def log_out(request):
    logout(request)
    return redirect('HomePage')

def TeacherSignup(request):
    form1=User_register()
    form2=TeachersReg()
    if request.method=='POST':
        form1=User_register(request.POST)
        form2=TeachersReg(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            user=form1.save(commit=False)
            user.is_teacher=True
            user.save()
            teacher=form2.save(commit=False)
            teacher.user=user
            teacher.save()
            return redirect('loginPage')
    return render(request,'TeachSignup.html',{'form1':form1,'form2':form2})
    
def signupPage(request):
    form1=User_register()
    form2=signup()
    if request.method=='POST':
        form1=User_register(request.POST)
        form2=signup(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            user=form1.save(commit=False)
            user.is_customer=True
            user.save()
            customer=form2.save(commit=False)
            customer.user=user
            customer.save()
            return redirect('loginPage')
    return render(request,'signup.html',{'form1':form1,'form2':form2})

def TeachersPage(request):
    return render(request,'Teachers.html')

def AdminPage(request):
    return render(request,'admin.html')

def student_page(request):
    return render(request,'StudentPage.html')

def view_teacher(request):
    data = TeachersLogin.objects.all()
    return render(request,'TeachersView.html',{'data':data})

def view_students(request):
    data=Customers.objects.all()
    return render(request,'StudentsView.html',{'data':data})

def delete_teacher(request,user_id):
    record=TeachersLogin.objects.get(user_id=user_id)
    record.delete()
    return redirect('view_teacher')

def delete_students(request,user_id):
    data = Customers.objects.get(user_id=user_id)
    data.delete()
    return redirect ('view_students')

def course_reg(request):
    form1=CourseReg()
    if request.method=='POST':
        form1=CourseReg(request.POST,request.FILES)
        if form1.is_valid():
            user=form1.save(commit=False)
            user.is_course=True
            user.save()
            return redirect('course_view')
    return render(request,'CourseReg.html',{'form1':form1})

def all_courses(request):
    course_data = Courses.objects.all()
    print(course_data)  # Debugging: Check if courses are available
    return render(request, 'AllCourses.html', {'course_data': course_data})
            
def course_view(request):
    course_data=Courses.objects.all()
    return render(request,'Courses.html',{'course_data':course_data})

def course_del(request, id):
    course_data = get_object_or_404(Courses, id=id)
    course_data.delete()
    return redirect('course_view')

def update_course(request, id):
    course = Courses.objects.get(id=id)
    form=CourseReg(instance=course)
    if request.method == 'POST':
        form = CourseReg(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_view')
    return render(request, 'CourseUpdate.html', {'form': form})

def class_list(request):
    classes= OnlineClass.objects.all()
    return render(request, 'OnlineClasses.html', {'classes':classes})

def class_details(request):
    class_obj=OnlineClass.objects.all()
    return render(request,'OnlineClassDet.html',{'class_obj':class_obj})

def UploadVideo(request):
    form1=Video()
    if request.method == 'POST':
        form1=Video(request.POST,request.FILES)
        if form1.is_valid():
            user=form1.save(commit=False)
            user.is_video=True
            user.save()
            return redirect('class_list')
    return render(request,'VideoUpload.html',{'form1':form1})

def del_video(request,id):
    data=OnlineClass.objects.get(id=id)
    data.delete()
    return redirect('class_list')

def update_class(request,id):
    on_class=OnlineClass.objects.get(id=id)
    form= Video(instance=on_class)
    if request.method=='POST':
        form=Video(request.POST,instance=on_class)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    return render(request,'ClassUpdate.html',{'form':form})

def study_materials(request):
    data = StudyMaterials.objects.all()
    return render(request, 'StudyMaterials.html', {'data': data})
            
def upload_notes(request):
    form1 = Materials()
    if request.method == 'POST':
        form1 = Materials(request.POST, request.FILES)
        if form1.is_valid():
            user = form1.save(commit=False)
            user.is_materials = True
            user.save()
            return redirect('study_materials')
    return render(request, 'UploadMaterials.html', {'form1': form1})
    
def del_file(request, id):
    data = StudyMaterials.objects.get(id=id)
    data.delete()
    return redirect('study_materials')

def download_file(request, id):
    file_object = get_object_or_404(StudyMaterials, id=id)
    file_content = file_object.pdf_notes.read()
    response = HttpResponse(file_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file_object.pdf_notes.name}"'
    return response

def Account_informations(request):
    return render(request,'MyProfile.html')

def student_page(request):
    course_data=Courses.objects.all()
    return render(request,'StudentPage.html',{'course_data':course_data})

def course_details(request, course_id):
    course = get_object_or_404(Courses, pk=course_id)
    return render(request, 'CourseDetails.html', {'course': course})

def MyProfile(request):
    # Assuming the user is logged in
    if request.user.is_authenticated:
        user_profile = Customers.objects.filter(user=request.user).first()
        if user_profile:
            context = {
                'first_name': user_profile.First_Name,
                'last_name': user_profile.Last_Name,
                'email': user_profile.Email,
                'phone_number': user_profile.Phone_Number,
                'district':user_profile.District,
                'state':user_profile.State,
                'image':user_profile.image,
            }
            return render(request, 'MyProfile.html', context)
    # Handle case when user is not logged in or profile doesn't exist
    return render(request, 'MyProfile.html', {})

def test_series(request):
    return render(request, 'testseries.html')

def user_videos(request):
    return render(request,'uservideos.html')

def live_classes(request):
    return render(request,'liveclasses.html')

def e_books(request):
    return render(request,'eBooks.html')

def my_orders(request):
    return render(request,'myOrders.html')

def my_wishlist(request):
    return render(request,'myWishlist.html')

@login_required
def buy(request, course_id):
    course = Courses.objects.get(pk=course_id)
    user = request.user
    purchase = Purchase(user=user, course=course, purchase_date=timezone.now())
    purchase.save()
    return redirect('success_page')

def success_page(request):
    return render(request, 'success.html')

def my_orders(request):
    # Retrieve purchases for the current user
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'myOrders.html', {'purchases': purchases})

def add_to_cart(request, course_id):
    if request.method == 'POST' and request.user.is_authenticated:
        course = Courses.objects.get(id=course_id)
        qty = 1  # Default quantity for now, you can change this as needed
        price = course.course_price  # Assuming course_price is the price field in Courses model

        # Create or update cart item
        cart_item, created = Cart_courses.objects.get_or_create(user=request.user, course=course, defaults={'qty': qty, 'price': price})

        if not created:
            cart_item.qty += qty
            cart_item.save()

        messages.success(request, f"{course.course_name} added to cart")
    elif not request.user.is_authenticated:
        messages.error(request, "You must be logged in to add items to cart")
    
    return redirect('all_courses')  # Redirect back to all_courses or any other page

def cart(request):
    cart_items = Cart_courses.objects.filter(user=request.user)
    total_amount = sum(item.qty * item.price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_amount': total_amount})

def remove_from_cart(request, cart_item_id):
    try:
        cart_item = Cart_courses.objects.get(id=cart_item_id)
        cart_item.delete()
        messages.success(request, "Item removed from cart")
    except Cart_courses.DoesNotExist:
        messages.error(request, "Item not found in cart")
    
    return redirect('cart')

def buy_items(request):
    if request.method == 'POST' and request.user.is_authenticated:
        cart_items = Cart_courses.objects.filter(user=request.user)
        if cart_items.exists():
            # Create an order for each item in the cart
            for item in cart_items:
                Order.objects.create(user=request.user, course=item.course, qty=item.qty, price=item.price)

            # Clear the cart
            cart_items.delete()

            messages.success(request, "Items purchased successfully")
        else:
            messages.error(request, "Your cart is empty")
    elif not request.user.is_authenticated:
        messages.error(request, "You must be logged in to buy items")

    return redirect('success_page')  # Redirect back to the cart page

def my_order(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        return render(request, 'myorders.html', {'orders': orders})
    else:
        # Handle the case where the user is not authenticated
        return render(request, 'myorders.html', {'orders': None})