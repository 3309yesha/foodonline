from django.shortcuts import render , get_object_or_404
from menu.models import Category , FoodItem
from vendor.models import vendor
from django.db.models import Prefetch
from .models import Cart
from django.http import HttpResponse , JsonResponse
from .context_processors import get_cart_counter, get_cart_amounts
from django.contrib.auth.decorators import login_required

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
        #  return JsonResponse({'status': 'success' , 'message': 'User is logged in.'})
        if request. headers. get( 'x-requested-with') == 'XMLHttpRequest' :
            try:
                #food item exist or not in fooditem table
                fooditem = FoodItem.objects.get(id=food_id)
                #print(fooditem)
                # check if user is already added that food to the cart
                try:
                    chkcart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # print(chkcart)
                    # increase the cart quantity
                    chkcart.quantity += 1
                    chkcart.save()
                    # print(chkcart.quantity)
                    return JsonResponse({'status': 'success' , 'message': 'Increase the cart quantity', 'cart_counter' : get_cart_counter(request), 'qty' : chkcart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    # print("hiii")
                    chkcart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    # print("hiii")
                    return JsonResponse({'status': 'success' , 'message': 'Added the food to the cart', 'cart_counter' : get_cart_counter(request), 'qty' : chkcart.quantity, 'cart_amount': get_cart_amounts(request)})
                    # print(chkcart.quantity)

            except:
                return JsonResponse({'status': 'Failed' , 'message': 'This food does no exist.'})
        else:
            return JsonResponse({'status': 'Failed' , 'message': 'Invalid request .'})
    else:
        return JsonResponse({'status': 'Login required !' , 'message': 'Please login to continue.'})

def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        #  return JsonResponse({'status': 'success' , 'message': 'User is logged in.'})
        if request. headers. get( 'x-requested-with') == 'XMLHttpRequest' :
            try:
                #food item exist or not in fooditem table
                fooditem = FoodItem.objects.get(id=food_id)
                #print(fooditem)
                # check if user is already added that food to the cart
                try:
                    chkcart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # print(chkcart)
                    if chkcart.quantity > 1:
                        # decrease the cart quantity
                        chkcart.quantity -= 1
                        chkcart.save()
                        # print(chkcart.quantity)
                    else:
                        chkcart.delete()
                        chkcart.quantity = 0
                    return JsonResponse({'status': 'success' , 'cart_counter' : get_cart_counter(request), 'qty': chkcart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    # print("hiii")
                    return JsonResponse({'status': 'Failed' , 'message': 'do not have any of the items' })
                    # print(chkcart.quantity)

            except:
                return JsonResponse({'status': 'Failed' , 'message': 'This food does no exist.'})
        else:
            return JsonResponse({'status': 'Failed' , 'message': 'Invalid request .'})
    else:
        return JsonResponse({'status': 'Login required !' , 'message': 'Please login to continue.'})
    # return HttpResponse(food_id)

@login_required(login_url = 'login')      
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html',context)



def delete_cart(request, cart_id):
     if request.user.is_authenticated:
        #  return JsonResponse({'status': 'success' , 'message': 'User is logged in.'})
        if request. headers. get( 'x-requested-with') == 'XMLHttpRequest' :
            try:
                #cart item in exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'success' , 'message': 'Your item deleted successfully', 'cart_counter' : get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed' , 'message': 'Cart item dose not exists!'})
        else:
            return JsonResponse({'status': 'Failed' , 'message': 'Invalid request!'})
