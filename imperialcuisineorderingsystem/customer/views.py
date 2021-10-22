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
        print(name, id)
        order = Order.objects.get(name=name);
        is_match = (order.verify({'name': name, 'id': id}))
        print(is_match)
        if (is_match):
            return redirect('order_detail', order_id=request.POST['order_id'])
        # print(order['name'])
        # if order['name'] == request.POST['name']:
            # If the name entered in the form matches the name on the order in the database, redirect to the order detail page
            # return redirect("order_detail", order_id=order['id'])
        # return render(request, 'login.html')
        # form = AuthenticationForm(request, request.POST)
        # if form.is_valid():
        # user = form.get_user()
        # login(request, user)
        # if 'next' in request.POST:
        # return
    # Query the database for an order with that name and id
        # Item.objects.create(id=34, my_order=1)
        # Item.objects.create(id=12, my_order=2)
        # Item.objects.create(id=4, my_order=3)
    # If they match, go ahead and give them assess to their order (render the order_detail.html, from which they should be able to either edit or delete their order as desired)
        # if order == 'Match':
        #     order_detail.update
    # If not, redirect back to home page (or however you want to handle that)
    #  return redirect("customer/about")
        # pass
    else:
        # return render('customer/about.html')
        # If not post request, then get request - render the pseudo-login page
         return render(request, "login.html")
        # pass
    # pass


def order_detail(request, order_id):
    # if it's a post request, go ahead and take the information from the request body and make the appropriate changes in the databasse
    if request.method == 'POST':
        pass
        # Query database for order with id passed in the url
        # orderId = request.POST.get('orderId', '')
        # try:
            # order = Order.objects.filter(pk=orderId)
            # if len(order) > 0:
                # update = Order.objects.filter(pk=orderId)
        # Update the row in the database to match the information passed in the form
        # updates = []
        # for order in update:
    else:
        order = Order.objects.get(id=order_id)
        return render(request, 'customer/order_detail.html', {'order': order})
        # If not a post requst, then it's a get request
        # Query the database for the order information
        # Render! That! Page!
        # return redirect("order_")


# def delete_order(request):
#     # Grab the order id (will probably be passed in the url, depending on how you set it up in urls.py and on your template)
#     order = Order.objects.get(id)
#     if request.method == "POST":
#         # Delete it from the database
#     order.delete()
#     # Redirect user back to home(?) page - or wherever you want to send them
#     return redirect('about')


# Create any templates you may still need (pseudo-login form, order detail page, order edit page, delete confirmation, whichever of these you want to include and/or anything else that makes sense to you)


# General todos for all of this:
# Connect these views to your urls.py
# If you need to add any links to access these new pages and routes to your existing navigation, do that
