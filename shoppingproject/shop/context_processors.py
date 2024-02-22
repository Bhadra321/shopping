from . models import CATEGORY,Cart,Cartitem
from . views import _cart_id
def menu_links(request):
    links=CATEGORY.objects.all()
    return dict(links=links)

def counter(request):
    item_count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart=Cart.objects.filter(cart_id=_cart_id(request))
            cart_items=Cartitem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                item_count += cart_item.quantity
        except:
            item_count =0
    return dict(item_count=item_count)                