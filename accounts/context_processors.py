from vendor.models import vendor
from .models import UserProfile

def get_vendor(request):
    try:
        Vendor = vendor.objects.get(user=request.user)
    except:
        Vendor = None
    return dict(vendor=Vendor) # do not change in any condition

def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user = request.user)
    except:
        user_profile = None    
    return dict(user_profile=user_profile) 