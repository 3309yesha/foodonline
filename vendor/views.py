from django.shortcuts import render
from .forms import VendorForm
from accounts.forms import UserProfileForm

from django.contrib import messages
from accounts.models import UserProfile
from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect,HttpResponse
from .models import vendor 
from menu.models import Category , FoodItem

from menu.forms import CategoryForm
from django.template.defaultfilters import slugify



from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor


# helper function for get vendor
def get_vendor(request):
    Vendor = vendor.objects.get(user=request.user)
    return Vendor

# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor) 
def vprofile(request):
    profile = get_object_or_404(UserProfile , user=request.user)
    Vendor = get_vendor(request)


    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=Vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Profile update successfully')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=profile)
    context = {
        'profile_form' : profile_form,
        'vendor_form' : vendor_form,
        'profile' : profile,
        'vendor' : Vendor
    }
    return render(request, 'vendor/vprofile.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor) 
def menu_builder(request):
    Vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=Vendor).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/menu_builder.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor) 
def fooditems_by_category(request, pk=None):
    Vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=Vendor, category=category)
    context = {
        'fooditems': fooditems,
        'category': category,
    }
    

    return render(request, 'vendor/fooditems_by_category.html', context)





def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            
            category.save() # here the category id will be generated
            category.slug = slugify(category_name)+'-'+str(category.id) # chicken-15
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)

    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)


def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)

    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'vendor/edit_category.html', context)


def delete_category(request, pk=None):
    category= get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'categroy has been deleted successfully!')
    return redirect('menu_builder')



