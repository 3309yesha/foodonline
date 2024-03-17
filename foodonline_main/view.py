from django.shortcuts import render
from django.http import HttpResponse
from vendor.models import vendor

def home(request):
    Vendors = vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    context = {
        'vendors': Vendors,
    }
    return render(request, 'home.html', context)