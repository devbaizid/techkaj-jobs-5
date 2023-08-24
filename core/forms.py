from django import forms
from .models import *



class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = [ 'name', 'email', 'cover_letter', 'bid_amount', 'cv_file']
        widgets = {
            'project': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Enter Project Name'}),
            'name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Enter Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Enter Your Email'}),
            'cover_letter': forms.Textarea(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Enter Your Cover Letter'}),
            'bid_amount': forms.NumberInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Enter Bid Amount'}),
            'cv_file': forms.FileInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Upload Your CV File'}),
        }
    def clean_cv_file(self):
        cv_file = self.cleaned_data['cv_file']
        allowed_filetypes = ['image/jpeg', 'image/png', 'application/pdf']

        if cv_file:
            if cv_file.content_type not in allowed_filetypes:
                raise forms.ValidationError("Invalid file format. Only JPG, PNG, and PDF files are allowed.")
            return cv_file

        else:
            raise forms.ValidationError("Please upload a valid file.")



class UpdateProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = [ 'name', 'email', 'cover_letter', 'bid_amount', 'cv_file']
        widgets = {
            'project': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Enter Project Name'}),
            'name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Enter Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Enter Your Email'}),
            'cover_letter': forms.Textarea(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Enter Your Cover Letter'}),
            'bid_amount': forms.NumberInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Enter Bid Amount'}),
            'cv_file': forms.FileInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Upload Your CV File'}),
        }
  



class SendProjectsFileForm(forms.ModelForm):
    class Meta:
        model = Send_Projects_file
        fields = ['file']

        widgets = {

            'file': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-[50px]  dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Upload Your CV File'}),
        }
  

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = contact_us
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'bg-gray-900  text-body-color border-[f0f0f0] focus:border-primary w-full rounded border py-3 px-[14px] text-base outline-none focus-visible:shadow-none',"placeholder":"Your Name"}),
            'email': forms.EmailInput(attrs={'class': 'bg-gray-900  text-body-color border-[f0f0f0] focus:border-primary w-full rounded border py-3 px-[14px] text-base outline-none focus-visible:shadow-none',"placeholder":"Your Email"}),
            'subject': forms.TextInput(attrs={'class': 'bg-gray-900  text-body-color border-[f0f0f0] focus:border-primary w-full rounded border py-3 px-[14px] text-base outline-none focus-visible:shadow-none',"placeholder":"your Subject"}),
            'message': forms.Textarea(attrs={'class': ' bg-gray-900  text-body-color border-[f0f0f0] focus:border-primary w-full rounded border py-3 px-[14px] text-base outline-none focus-visible:shadow-none','placeholder':"Your Message"}),
        }


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from django import forms
from .models import Pay_out_money

class EditBkashMoneyForm(forms.ModelForm):
    destination_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full rounded-md border mt-2 mb-1 border-gray-500 bg-white p-3 text-gray-700 shadow-sm transition focus:border-gray-300 focus:outline-none focus:ring focus:ring-blue-400'}))
    destination_phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full rounded-md border mt-2 mb-1 border-gray-500 bg-white p-3 text-gray-700 shadow-sm transition focus:border-gray-300 focus:outline-none focus:ring focus:ring-blue-400'}))
    destination_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full rounded-md border mt-2 mb-1 border-gray-500 bg-white p-3 text-gray-700 shadow-sm transition focus:border-gray-300 focus:outline-none focus:ring focus:ring-blue-400'}))
    # paypal_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full rounded-md border mt-2 mb-1 border-gray-500 bg-white p-3 text-gray-700 shadow-sm transition focus:border-gray-300 focus:outline-none focus:ring focus:ring-blue-400'}))
    # paypal_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full rounded-md border mt-2 mb-1 border-gray-500 bg-white p-3 text-gray-700 shadow-sm transition focus:border-gray-300 focus:outline-none focus:ring focus:ring-blue-400'}))
    # account_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full rounded-md border mt-2 mb-1 border-gray-500 bg-white p-3 text-gray-700 shadow-sm transition focus:border-gray-300 focus:outline-none focus:ring focus:ring-blue-400'}))
    # account_holder_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full rounded-md border mt-2 mb-1 border-gray-500 bg-white p-3 text-gray-700 shadow-sm transition focus:border-gray-300 focus:outline-none focus:ring focus:ring-blue-400'}))
    # bank_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full rounded-md border mt-2 mb-1 border-gray-500 bg-white p-3 text-gray-700 shadow-sm transition focus:border-gray-300 focus:outline-none focus:ring focus:ring-blue-400'}))
    # routing_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full rounded-md border mt-2 mb-1 border-gray-500 bg-white p-3 text-gray-700 shadow-sm transition focus:border-gray-300 focus:outline-none focus:ring focus:ring-blue-400'}))
# 'paypal_name','paypal_email','account_number','account_holder_name','bank_name','routing_number'

    class Meta:
        model = Pay_out_money
        fields = ['destination_name','destination_phone','destination_address']




class EditBankMoneyForm(forms.ModelForm):
  
    # paypal_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full rounded-md border mt-2 mb-1 border-gray-500 bg-white p-3 text-gray-700 shadow-sm transition focus:border-gray-300 focus:outline-none focus:ring focus:ring-blue-400'}))
    # paypal_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full rounded-md border mt-2 mb-1 border-gray-500 bg-white p-3 text-gray-700 shadow-sm transition focus:border-gray-300 focus:outline-none focus:ring focus:ring-blue-400'}))
    account_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full rounded-md border mt-2 mb-1 border-gray-500 bg-white p-3 text-gray-700 shadow-sm transition focus:border-gray-300 focus:outline-none focus:ring focus:ring-blue-400'}))
    account_holder_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full rounded-md border mt-2 mb-1 border-gray-500 bg-white p-3 text-gray-700 shadow-sm transition focus:border-gray-300 focus:outline-none focus:ring focus:ring-blue-400'}))
    bank_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full rounded-md border mt-2 mb-1 border-gray-500 bg-white p-3 text-gray-700 shadow-sm transition focus:border-gray-300 focus:outline-none focus:ring focus:ring-blue-400'}))
    routing_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full rounded-md border mt-2 mb-1 border-gray-500 bg-white p-3 text-gray-700 shadow-sm transition focus:border-gray-300 focus:outline-none focus:ring focus:ring-blue-400'}))
# 'paypal_name','paypal_email','account_number','account_holder_name','bank_name','routing_number'

    class Meta:
        model = Pay_out_money
        fields = ['account_number','account_holder_name','bank_name','routing_number']




class EditPaypalMoneyForm(forms.ModelForm):
  
    paypal_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full rounded-md border mt-2 mb-1 border-gray-500 bg-white p-3 text-gray-700 shadow-sm transition focus:border-gray-300 focus:outline-none focus:ring focus:ring-blue-400'}))
    paypal_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full rounded-md border mt-2 mb-1 border-gray-500 bg-white p-3 text-gray-700 shadow-sm transition focus:border-gray-300 focus:outline-none focus:ring focus:ring-blue-400'}))
 
# 'paypal_name','paypal_email','account_number','account_holder_name','bank_name','routing_number'

    class Meta:
        model = Pay_out_money
        fields = ['paypal_name','paypal_email']
