from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from .models import Feedback
from .models import PortfolioProject
from .models import Feedback
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
def index(request):
    # Fetch feedback sorted by newest
    feedback_list = Feedback.objects.all().order_by('-created_at')

    # Include the feedback list in the context
    context = {
        'feedback_list': feedback_list,
    }
    
    return render(request, 'index.html', context)
@login_required(login_url='/login/', redirect_field_name='next')
def Pack(request):
    return render(request, 'pack.html')
def do(request):
    return render(request, 'do.html')
def about(request):
    return render(request, 'about.html')

@login_required
@user_passes_test(lambda user: user.is_superuser)  # Restrict to superuser
def portf(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        # Check if all fields are received
        if not all([title, description, image]):
            return HttpResponse("Error: Missing fields. Please fill all fields.")

        try:
            # Save to the database
            PortfolioProject.objects.create(
                title=title,
                description=description,
                image=image
            )
            return redirect('portfolio2')  # Redirect to clear the form or to a success page
        except Exception as e:
            return HttpResponse(f"Error: {e}")

    return render(request, 'proj_upload.html')
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Changed to username
        password = request.POST.get('password')
        
        # Authenticate using the username and password
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('/')  # Redirect to home or dashboard
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('/login/')
    
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/register/')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "User with this email already exists.")
            return redirect('/register/')
        
        user = User.objects.create_user(username=email, email=email, first_name=name, password=password)
        user.save()
        messages.success(request, "Registration successful. Please login.")
        return redirect('/login/')
    
    return render(request, 'reg.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('/login/')

def Port(request):
    projects = PortfolioProject.objects.all()
    return render(request, 'portfolio.html', {'projects': projects})

def contact_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if full_name and phone_number and email and message:
            Contact.objects.create(
                full_name=full_name,
                phone_number=phone_number,
                email=email,
                message=message
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
        else:
            messages.error(request, "Please fill in all fields.")
    
    return render(request, 'index.html')



def feedback_view(request):
    feedback_list = Feedback.objects.all().order_by('-created_at')  # Fetch feedback sorted by newest
    context = {
        'feedback_list': feedback_list,
    }
    return render(request, 'feedback.html', context)

@login_required
@user_passes_test(lambda user: user.is_superuser)  # Restrict to superuser
def admin_panel(request):
    return render(request, 'admin.html')



def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # Check if the user has staff/admin rights
            login(request, user)
            return redirect('admin_panel')  # Redirect to your admin panel
        else:
            messages.error(request, 'Invalid credentials or unauthorized access.')
    return render(request, 'admlogin.html')




@login_required
@user_passes_test(lambda user: user.is_superuser)  # Restrict to superuser
def contact_view2(request):
    contacts = Contact.objects.all()  # Fetch all contacts from the database
    return render(request, 'cont_view.html', {'contacts': contacts})


@login_required
def feedback_upload(request):
    if request.method == "POST":
        name = request.POST.get('name')
        designation = request.POST.get('designation')
        quote = request.POST.get('quote')
        image = request.FILES.get('image')

        # Validate inputs if needed (optional)
        if not name or not quote or not image:
            messages.error(request, "All fields are required except Designation.")
            return render(request, 'feedback_upload.html')

        # Create Feedback instance
        Feedback.objects.create(
            name=name,
            designation=designation,
            quote=quote,
            image=image
        )
        messages.success(request, "Feedback successfully uploaded!")
        return redirect('feedback_upload')

    return render(request, 'fed_upload.html')