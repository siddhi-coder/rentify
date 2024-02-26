from django import forms
from .models import RentalRequest , Car_Product

class Step1Form(forms.Form):
    pickup_location = forms.CharField(max_length=100)
    pickup_date = forms.DateField()

class Step2Form(forms.Form):
    return_location = forms.CharField(max_length=100)
    return_date = forms.DateField()

class Step3Form(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        carproductid = kwargs.pop('carproductid', None)
        super(Step3Form, self).__init__(*args, **kwargs)
        self.fields['carproductid'] = forms.ModelChoiceField(queryset=Car_Product.objects.all(), label='Car Product')

    def clean(self):
        cleaned_data = super().clean()
        carproductid = cleaned_data.get('carproductid')
        if not carproductid:
            raise forms.ValidationError('Please select a valid Car Product.')
        return cleaned_data

class PaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    currency = forms.CharField(max_length=3, initial='TRY')

