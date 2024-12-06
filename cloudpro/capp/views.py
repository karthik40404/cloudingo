from django.contrib.auth import authenticate, login, logout 
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import UserFile
from .forms import FileUploadForm
from django.contrib import messages 
import os

def login_user(request):
    # Redirect to the upload page if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('upload_file')  # Redirect to the upload page if already logged in

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        # Check if the user exists and the credentials are correct
        if user is not None:
            login(request, user)  # Log the user in
            return redirect('upload_file')  # Redirect to the upload page after login
        else:
            # If credentials are incorrect, show an error message
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    # If the request method is GET, just render the login page
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # Redirect to login page after registration
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def upload_file(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user_file = form.save(commit=False)
            user_file.user = request.user  # Associate file with the logged-in user
            user_file.save()
            return redirect('list_files')
    else:
        form = FileUploadForm()
    return render(request, 'upload_file.html', {'form': form})

# def list_files(request):
#     if not request.user.is_authenticated:
#         return redirect('login')  

#     files = UserFile.objects.filter(user=request.user)  
#     return render(request, 'list_files.html', {'files': files})

def file_list(request):
    user_files = UserFile.objects.filter(user=request.user) 
    images = user_files.filter(category='image')
    videos = user_files.filter(category='video')
    other_files = user_files.filter(category='file')

    return render(request, 'list_files.html', {
        'images': images,
        'videos': videos,
        'other_files': other_files,
    })

def delete_file(request, file_id):
    file = get_object_or_404(UserFile, id=file_id, user=request.user)
    file_path = file.file.path  
    file.delete()
    try:
        os.remove(file_path)  
    except FileNotFoundError:
        pass  
    
    return redirect('list_files')  