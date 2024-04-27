from django.shortcuts import render, redirect
from .models import Recipe
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from rest_framework.authentication import BasicAuthentication
# from rest_framework.permissions import IsAuthenticated   # authorization
from django.conf import Settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache  import cache_page
from django.core.cache import cache

CACHE_TTL = getattr(Settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# Create your views here. 
def add_reciepes(request):

   
    data = request.POST
    if request.method == 'POST':
        data = request.POST

        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')
       

        Recipe.objects.create(
            recipe_name = recipe_name,
            recipe_description = recipe_description,
            recipe_image = recipe_image
        )
        return redirect('/recipe/')
    
    # cache_data = cache.get('recipe_name')
    # if cache_data:
    #     cache_data = Recipe.objects.all()
    #     cache.set('recipe_name', cache_data, timeout=CACHE_TTL)
    #     print("cache-data")
    #     print(cache_data)

    # if request.GET.get('Search'):
    #     queryset = queryset.filter(recipe_name__icontains=request.GET.get('Search'))
    QuerySet = Recipe.objects.all()

    if request.GET.get('Search'):
        QuerySet= QuerySet.filter(recipe_name__icontains = request.GET.get('Search'))
    return render(request,'template/recipi.html', context={'Recipe': QuerySet})

# def my_view(request):
#     data = cache.get('my_data')
#     if data is None:
#         # data = 
#         cache.set('my_data', data, timeout=CACHE_TTL)
# def get_reciepe():

def delete_item(request,id):
    data = Recipe.objects.get(id = id)
    data.delete()
    return redirect('/recipe/')

def update_item(request,id):
    object = Recipe.objects.get(id=id)
    if request.method == 'POST':
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')

        object.recipe_name = recipe_name
        object.recipe_description = recipe_description 
        if recipe_image:
            object.recipe_image = recipe_image
        object.save()
        return redirect('/recipe/')

    return render(request,'template/update.html',context={'object': object})


def login_user(request):
    if request.method == 'POST':
        username =request.POST.get('username')
        password =request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request, 'Invalid Username')
            return redirect('/login/')
        
        user = authenticate(username = username, password = password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/recipe/')



        
    return render(request,'template/login.html')

def register(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, 'Username already exists')
            return redirect('/register/')

        try:
            user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            # password = password
          )
            user.set_password(password)
            user.save()
            messages.info(request,'Account created successfully!!!!')
            return redirect('/register/')
        except IntegrityError:           
         return render(request,'template/register.html',content_type={'error': 'error'})
    return render(request,'template/register.html') 
        

def logout_page(request):
     logout(request)
     return redirect('/login/')


def user_register(request):
    if request.method == 'POST':
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        