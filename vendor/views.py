from django.shortcuts import render
from .forms import VendorForm
from accounts.forms import UserProfileForm

from django.contrib import messages
from accounts.models import UserProfile
from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect,HttpResponse
from .models import vendor






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

