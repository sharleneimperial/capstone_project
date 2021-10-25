from django.forms import ModelForm
from .models import Order

class Order_Form(ModelForm):
    class Meta:
        model = Order
        fields = ['street', 'city', 'state']