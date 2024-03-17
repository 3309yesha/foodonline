from django.shortcuts import render , get_object_or_404
from menu.models import Category , FoodItem
from vendor.models import vendor
from django.db.models import Prefetch
from .models import Cart
from django.http import HttpResponse , JsonResponse
from .context_processors import get_cart_counter

# Create your views here.
def marketplace(request):
    Vendors = vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = Vendors.count()
    context = {
        'vendors': Vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)



def vendor_detail(request, vendor_slug):
    Vendor = get_object_or_404(vendor, vendor_slug=vendor_slug)

    categories = Category.objects.filter(vendor=Vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': Vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request. headers. get( 'x-requested-with') == 'XMLHttpRequest' :
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                     # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity','cart_counter': get_cart_counter(request), 'qty': chkCart.quantity})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart','cart_counter': get_cart_counter(request), 'qty': chkCart.quantity})
            except:
                return JsonResponse({'status': 'Success', 'message': 'This food does not exits!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})       
        

def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request. headers. get( 'x-requested-with') == 'XMLHttpRequest' :
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chkCart.quantity > 1: 
                        # decrease  the cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'Success','cart_counter': get_cart_counter(request), 'qty': chkCart.quantity})
                except:
                    return JsonResponse({'status': 'Failed', 'message':'You do not have this item in ypur cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exits!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})       

