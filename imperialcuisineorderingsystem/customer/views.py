from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.core.mail import send_mail
from .models import MenuItem, Category, Order
from django.contrib.auth.forms import AuthenticationForm


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


class Order_View(View):
    def get(self, request, *args, **kwargs):
        pass
        # retrieving every item from each category
        appetizers = MenuItem.objects.filter(
            category__name__contains='Appetizer')
        entrees = MenuItem.objects.filter(category__name__contains='Entree')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # then passing it into context
        context = {
            'appetizers': appetizers,
            'entrees': entrees,
            'desserts': desserts,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')
        print(Order)
        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=item)
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = Order.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )
        order.items.add(*item_ids)

        # When all is finished, then send confirmation email to the User
        body = ('Thank you so much for your order! We are preparing your food and will be delivered to you soon!\n'
                f'Your total: {price}\n'
                'Thank you once again for your order!')

        send_mail('Thank You So Much For Your Order!',
                  body,
                  'imperial@imperial.com',
                  [email],
                  fail_silently=False
                  )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request, 'customer/order_confirmation.html', context)


class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)

def access_order(request):
    if request.method == 'POST':
        name = request.POST['name']
        id = int(request.POST['order_id'])
        order = Order.objects.get(id=id)
        is_match = (order.verify({'name': name, 'id': id}))
        if (is_match):
            return redirect('order-details', order_id=request.POST['order_id'])

    return render(request, "login.html")


def order_detail(request, order_id):
    # if it's a post request, go ahead and take the information from the request body and make the appropriate changes in the databasse
    if request.method == 'POST':
        # Query database for order with id passed in the url
        order = Order.objects.get(id=order_id)

        # Update the order with the information from the form being posted

        # Redirect to whatever page you want users to go to after updating their order

        # Remove pass line after once you've added your return statement
        pass
    else:
        # Right now this is set up to just present the items in the order to the user
        # You may also want to send the order's address to the detail page, if you want to add the ability to change that address
        order = Order.objects.get(id=order_id)
        order_items = MenuItem.objects.filter(id__in=order.items.all())
        print(order_items)
        return render(request, 'customer/order_detail.html', {'items': order_items, 'order_id': order_id})


def delete_order(request, order_id):
    # Grab the order id (will probably be passed in the url, depending on how you set it up in urls.py and on your template)
    order = Order.objects.get(id=order_id)
    # if request.method == "POST":
        # Delete it from the database
    order.delete()
    # Redirect user back to home(?) page - or wherever you want to send them
    return redirect('about')

def update_order(request, order_id):

    order = Order.objects.get(id=order_id)
    order.update()
    return redirect('order_detail')


# Create any templates you may still need (pseudo-login form, order detail page, order edit page, delete confirmation, whichever of these you want to include and/or anything else that makes sense to you)


# General todos for all of this:
# Connect these views to your urls.py
# If you need to add any links to access these new pages and routes to your existing navigation, do that
