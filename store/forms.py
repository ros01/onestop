from django import forms
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Item, Category, Vendor, Issue
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.utils import timezone
from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_modal_forms.mixins import PassRequestMixin, PopRequestMixin, CreateUpdateAjaxMixin






class ItemModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:
        model = Item
        fields = ('item_name', 'item_description', 'category', 'stock_code', 'vendor', 'unit', 'quantity', 'unit_price', 're_order_no', 'item_image', 'entered_by',)

        widgets = {
        
        'item_description': forms.Textarea(attrs={'rows':2, 'cols':12}),
        
        
        }
                

    def __init__(self, *args, **kwargs):
       super(ItemModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
       self.fields['item_name'].label = "Item Name"
       self.fields['item_name'].widget.attrs['placeholder'] = "Item Name"
       self.fields['item_description'].label = "Description"
       self.fields['item_description'].widget.attrs['placeholder'] = "Enter brief description of item"
       self.fields['category'].label = "Category"
       self.fields['category'].widget.attrs['placeholder'] = "Choose"
       self.fields['unit'].label = "Unit of Measurement"
       self.fields['unit'].widget.attrs['placeholder'] = "Enter a unit of Measurement"
       self.fields['unit_price'].label = "Unit Price"
       self.fields['unit_price'].widget.attrs['placeholder'] = "Enter purchase price of Item"
       self.fields['re_order_no'].label = "Re-order No"
       self.fields['re_order_no'].widget.attrs['placeholder'] = "Enter Item Re-order Level"

    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance




class CategoryModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:
        model = Category
        fields = ('category_name', 'description',)

        widgets = {
        
        'description': forms.Textarea(attrs={'rows':2, 'cols':12}),
        
        
        }
                

    def __init__(self, *args, **kwargs):
       super(CategoryModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
       self.fields['category_name'].label = "Category Name"
       self.fields['category_name'].widget.attrs['placeholder'] = "Category Name"
       self.fields['description'].label = "Description"
       self.fields['description'].widget.attrs['placeholder'] = "Enter brief category description"


    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance
       
       
       
class VendorModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:
        model = Vendor
        fields = ('vendor_name', 'address', 'phone', 'email', 'description',)

        widgets = {
        
        'description': forms.Textarea(attrs={'rows':2, 'cols':12}),
        
        
        }
                

    def __init__(self, *args, **kwargs):
       super(VendorModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
       self.fields['vendor_name'].label = "Vendor Name"
       self.fields['vendor_name'].widget.attrs['placeholder'] = "Vendor Name"
       self.fields['address'].label = "Vendor Address"
       self.fields['address'].widget.attrs['placeholder'] = "Vendor Address"
       self.fields['phone'].label = "Phone No"
       self.fields['phone'].widget.attrs['placeholder'] = "Phone No"
       self.fields['email'].label = "Email"
       self.fields['email'].widget.attrs['placeholder'] = "Vendor email"
       self.fields['description'].label = "Description"
       self.fields['description'].widget.attrs['placeholder'] = "Enter brief description of Vendor"

    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance


       
class IssueRequisitionModelForm(forms.ModelForm):


    class Meta:
        model = Issue

        fields = ('requisition_no', 'item', 'department', 'requisition_date', 'quantity_requested','quantity_issued', 'requesting_staff', 'issued_by',)

        widgets = {
        'department': forms.HiddenInput(),
        'requisition_date': forms.HiddenInput(),   
        'requesting_staff': forms.HiddenInput(),
        'item': forms.TextInput(attrs={'readonly': True}),
        'requisition_no': forms.TextInput(attrs={'readonly': True}), 
        'quantity_requested': forms.TextInput(attrs={'readonly': True}),

        }

        

    def __init__(self, *args, **kwargs):
       super(IssueRequisitionModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
      
       self.fields['requisition_no'].label = "Requisition No"
       self.fields['item'].label = "Item Name"
       self.fields['item'].widget.attrs['placeholder'] = "Item Name"
       self.fields['department'].label = "Department"
       self.fields['requisition_date'].label = "Requisition Date"
       self.fields['quantity_requested'].label = "Requested Quantity"
       self.fields['quantity_issued'].label = "Quantity Issued"
       self.fields['quantity_issued'].widget.attrs['placeholder'] = "Enter Issue Quantity"
       self.fields['requesting_staff'].label = "Requesting Staff"
       self.fields['requesting_staff'].widget.attrs['placeholder'] = "Requesting Staff"
       self.fields['issued_by'].label = "Issueing Officer"
       self.fields['issued_by'].widget.attrs['placeholder'] = "Issuing Officer"



    


