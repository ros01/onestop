from django import forms
from django.forms import formset_factory, modelformset_factory, inlineformset_factory, BaseInlineFormSet
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.utils import timezone
from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_modal_forms.mixins import PassRequestMixin, PopRequestMixin, CreateUpdateAjaxMixin
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.auth import get_user_model
User = get_user_model()


class ItemFilterForm(forms.Form):
    q = forms.CharField(label='Search', required=False)
    # category_id = forms.ModelMultipleChoiceField(
    #     label='Category',
    #     queryset=Category.objects.all(), 
    #     widget=forms.CheckboxSelectMultiple, 
    #     required=False)
    
    # max_price = forms.DecimalField(decimal_places=2, max_digits=12, required=False)
    # min_price = forms.DecimalField(decimal_places=2, max_digits=12, required=False)



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


class InventoryItemsModelForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('item_name', 'item_description', 'category', 'stock_code', 'vendor', 'unit', 'quantity', 'unit_price', 're_order_no', 'item_image', 'entered_by',)

        widgets = {
        'item_description': forms.Textarea(attrs={'rows':2, 'cols':12}),  
        }          

    def __init__(self, *args, **kwargs):
       super(InventoryItemsModelForm, self).__init__(*args, **kwargs)
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

    



class RequisitionModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    #items = forms.ModelChoiceField(queryset=Item.objects.all(), empty_label=None, widget=forms.CheckboxSelectMultiple(),)
    class Meta:
        model = Requisition
        # fields = ('items', 'requisition_reason', 'requesting_staff', 'authorized_by', 'department',)
        fields = ('requisition_reason', 'employee', 'hod', 'department',)

        widgets = {
        'requisition_reason': forms.Textarea(attrs={'rows':2, 'cols':12}),  
        }  

    def __init__(self, *args, **kwargs):
       super(RequisitionModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       #self.fields['items'].label = "Requisition Items"
       #self.fields['items'].widget.attrs['placeholder'] = "Requisition Items"
       #self.fields['items'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)
       
       # self.fields['items'].label = "Requisition Items"
       # self.fields['items'].widget = CheckboxSelectMultiple()
       # self.fields['items'].queryset = Item.objects.all()

       self.fields['requisition_reason'].label = "Requisition Reason"
       self.fields['requisition_reason'].widget.attrs['placeholder'] = "Enter Reason for Requesting Items"
       self.fields['employee'].label = "Requesting Staff"
       self.fields['employee'].widget.attrs['placeholder'] = "Choose"
       self.fields['department'].label = "Department"
       self.fields['department'].widget.attrs['placeholder'] = "Enter Staff Department"
       self.fields['hod'].label = "Requisition Authorized By"
       self.fields['hod'].widget.attrs['placeholder'] = "Choose"
       
    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance




class RequisitionsModelForm(forms.ModelForm):
    #items = forms.ModelChoiceField(queryset=Item.objects.all(), empty_label=None, widget=forms.CheckboxSelectMultiple(),)
    class Meta:
        model = Requisition
        fields = ('requisition_reason', 'department', 'employee', 'hod', )

        widgets = {
        'requisition_reason': forms.Textarea(attrs={'rows':2, 'cols':12}),  
        
        }
    

    def __init__(self, *args, **kwargs):
       super(RequisitionsModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       
       self.fields['requisition_reason'].label = "Requisition Reason"
       self.fields['requisition_reason'].widget.attrs['placeholder'] = "Enter Reason for Requesting Items"
       self.fields['employee'].label = "Requesting Staff"
       # self.fields['employee'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)
       self.fields['department'].label = "Department"
       self.fields['department'].widget.attrs['placeholder'] = "Enter Staff Department"
       self.fields['hod'].label = "Requisition Authorized By"
       # self.fields['hod'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)
       # self.fields['requesting_staff'].queryset = User.objects.none()
       # self.fields['employee'].queryset =Employee.objects.none()
       # self.fields['hod'].queryset =Employee.objects.none()


       # if 'department' in self.data:
       #      try:
       #          department_id = int(self.data.get('department'))
       #          self.fields['employee'].queryset = Employee.objects.filter(department_id=department_id)
       #          self.fields['hod'].queryset = Employee.objects.filter(department_id=department_id)
       #      except (ValueError, TypeError):
       #          pass  # invalid input from the client; ignore and fallback to empty city queryset
       # elif self.instance.pk:
       #      try:
       #          self.fields['employee'].queryset = Employee.objects.all()
       #          self.fields['hod'].queryset = Employee.objects.all()
       #      except (ValueError, TypeError):
       #          pass  

       # else:
       #      pass 


       # else:
       #      try:
       #          self.fields['employee'].queryset = self.instance.department.user_set.order_by('email')
       #          self.fields['hod'].queryset = self.instance.department.user_set.order_by('email')
       #      except (ValueError, TypeError):
       #          pass
  

class RequisitionCartItemModelForm(forms.ModelForm):
    #items = forms.ModelChoiceField(queryset=Item.objects.all(), empty_label=None, widget=forms.CheckboxSelectMultiple(),)
    class Meta:
        model = RequisitionCartItem
        fields = ( 'requisition_cart', 'item', 'quantity')


    def __init__(self, *args, **kwargs):
       super(RequisitionItemModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       
       self.fields['requisition'].label = "Requisition"
       self.fields['requisition'].widget.attrs['placeholder'] = "Requisition"
       self.fields['item'].label = "Item Name"
       self.fields['item'].widget.attrs['placeholder'] = "Item Name"
       self.fields['quantity'].label = "Quantity"
       self.fields['quantity'].widget.attrs['placeholder'] = "Quantity"
       
    

RequisitionItemFormSet = modelformset_factory(RequisitionCartItem, fields=('requisition_cart', 'item', 'quantity',), can_delete=True)

class RequisitionsUpdateModelForm(forms.ModelForm):
    #items = forms.ModelChoiceField(queryset=Item.objects.all(), empty_label=None, widget=forms.CheckboxSelectMultiple(),)
    class Meta:
        model = Requisition
        fields = ('requisition_reason', 'department', 'employee', 'hod', )

        widgets = {
        'requisition_reason': forms.Textarea(attrs={'rows':2, 'cols':12}),  
        
        }
    

    def __init__(self, *args, **kwargs):
       super(RequisitionsUpdateModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       
       self.fields['requisition_reason'].label = "Requisition Reason"
       self.fields['requisition_reason'].widget.attrs['placeholder'] = "Enter Reason for Requesting Items"
       self.fields['employee'].label = "Requesting Staff"
       # self.fields['employee'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)
       self.fields['department'].label = "Department"
       self.fields['department'].widget.attrs['placeholder'] = "Enter Staff Department"
       self.fields['hod'].label = "Requisition Authorized By"
       # self.fields['hod'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)
       # self.fields['employee'].queryset = User.objects.none()


       # if 'department' in self.data:
       #      try:
       #          department_id = int(self.data.get('department'))
       #          self.fields['employee'].queryset = User.objects.filter(department_id=department_id)
       #          self.fields['hod'].queryset = User.objects.filter(department_id=department_id)
       #      except (ValueError, TypeError):
       #          pass  # invalid input from the client; ignore and fallback to empty city queryset
       # elif self.instance.pk:
       #      try:
       #          self.fields['employee'].queryset = User.objects.all()
       #          self.fields['hod'].queryset = User.objects.all()
       #      except (ValueError, TypeError):
       #          pass   
       # else:
       #      try:
       #          self.fields['employee'].queryset = self.instance.department.user_set.order_by('email')
       #          self.fields['hod'].queryset = self.instance.department.user_set.order_by('email')
       #      except (ValueError, TypeError):
       #          pass
 
class RequisitionItemForm(forms.ModelForm):
    class Meta:
        model = RequisitionCartItem
        exclude = ()


class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        exclude = ('requisition_date', 'requisition_status',)


# RequisitionFormSet = inlineformset_factory(
#                                         RequisitionItem, 
#                                         Requisition, 
#                                         fields = ['requisition', 'item', 'quantity'], 
#                                         exclude = [], 
#                                         can_delete = True,
#                                         extra=1,
#                                         )
   

# class Role(models.Model): # for each role there can be multiple users
#     role_name=models.CharField(max_length=20)

# class User(models.Model): # each user can have multiple roles
#     name=models.CharField(max_length=20)
#     role=models.ManyToManyField(Role, through='UserRole')

# class UserRole(models.Model): # table to store which user has which roles
#     role=models.ForeignKey(Role)
#     user=models.ForeignKey(User)      
    

# class UserForm(ModelForm):
#     class Meta:
#         model = User

# RoleFormSet = inlineformset_factory(User, Role) 
# RoleFormSet = inlineformset_factory(UserRole, User.role.through)



class CategoryModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:
        model = Category
        fields = ('category_name', 'category_short','description',)

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


       
class IssueRequisitionModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = IssueRequisition
        fields = ('requisition', 'issued_by',)
         # 'item_name', 'department', 'requisition_date', 'quantity_requested','quantity_issued', 'requesting_staff', 'issued_by',)
        widgets = {
        # 'department': forms.HiddenInput(),
        # 'requisition_date': forms.HiddenInput(),   
        # 'requesting_staff': forms.HiddenInput(),
        'requisition': forms.TextInput(attrs={'readonly': True}), 
        # 'quantity_requested': forms.TextInput(attrs={'readonly': True}),
        }   

    def __init__(self, *args, **kwargs):
       super(IssueRequisitionModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            }) 
       self.fields['requisition'].label = "Requisition"
       # self.fields['item_name'].widget.attrs['value'] = self.instance.item_name
       # self.fields['item_name'].widget.attrs['readonly'] = 'readonly'
       # self.fields['item_name'].label = "Item Name"
       # self.fields['department'].label = "Department"
       # self.fields['requisition_date'].label = "Requisition Date"
       # self.fields['quantity_requested'].label = "Requested Quantity"
       # self.fields['quantity_issued'].label = "Quantity Issued"
       # self.fields['quantity_issued'].widget.attrs['placeholder'] = "Enter Issue Quantity"
       # self.fields['requesting_staff'].label = "Requesting Staff"
       # self.fields['requesting_staff'].widget.attrs['placeholder'] = "Requesting Staff"
       # self.fields['issued_by'].label = "Issueing Officer"
       # self.fields['issued_by'].widget.attrs['placeholder'] = "Issuing Officer"

    def save(self):
      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)
      return instance

class IssueRequisitionItemModelForm(forms.ModelForm):
    class Meta:
        model = RequisitionCartItem
        fields = ('item', 'quantity', 'quantity_issued')
      
        widgets = {
        # 'requesting_staff': forms.HiddenInput(),
        # 'requisition': forms.TextInput(attrs={'readonly': True}), 
        # 'quantity_requested': forms.TextInput(attrs={'readonly': True}),
        'quantity_issued': forms.NumberInput(attrs={'class':'form-control'}), 
        }   

    def __init__(self, *args, **kwargs):
       super(IssueRequisitionItemModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            }) 
      
       # self.fields['requisition'].widget.attrs['value'] = self.instance.requisition
       self.fields['item'].widget.attrs['readonly'] = 'readonly'
       self.fields['item'].label = "Item"
       self.fields['quantity'].widget.attrs['readonly'] = 'readonly'
       self.fields['quantity'].label = "Quantity Requested"
       # self.fields['quantity'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)


#IssueRequisitionItemFormSet = modelformset_factory(RequisitionCartItem, form=IssueRequisitionItemModelForm, can_delete=False, extra=0)

class RequisitionCartModelForm(forms.ModelForm):
    class Meta:
        model = RequisitionCart
        fields = ('employee', 'requisition_no')
      
        widgets = {
        # 'requesting_staff': forms.HiddenInput(),
        # 'requisition': forms.TextInput(attrs={'readonly': True}), 
        # 'quantity_requested': forms.TextInput(attrs={'readonly': True}),
        # 'quantity_issued': forms.NumberInput(attrs={'class':'form-control'}), 
        }   

    def __init__(self, *args, **kwargs):
       super(RequisitionCartModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            }) 
      
       # self.fields['requisition'].widget.attrs['value'] = self.instance.requisition
       # self.fields['item'].widget.attrs['readonly'] = 'readonly'
       # self.fields['item'].label = "Item"
       # self.fields['quantity'].widget.attrs['readonly'] = 'readonly'
       # self.fields['quantity'].label = "Quantity Requested"
       # self.fields['quantity'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)



class IssueRequisitionsModelForm(forms.ModelForm):
    class Meta:
        model = IssueRequisition
        fields = ('requisition', 'issued_by')
         # 'item_name', 'department', 'requisition_date', 'quantity_requested','quantity_issued', 'requesting_staff', 'issued_by',)
        widgets = {
        'issued_by': forms.HiddenInput(),
        # 'requisition_date': forms.HiddenInput(),   
        # 'requesting_staff': forms.HiddenInput(),
        # 'requisition': forms.TextInput(attrs={'readonly': True}), 
        # 'quantity_requested': forms.TextInput(attrs={'readonly': True}),
        }   

    def __init__(self, *args, **kwargs):
       super(IssueRequisitionsModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            }) 
      
       # self.fields['requisition'].widget.attrs['value'] = self.instance.requisition
       self.fields['requisition'].widget.attrs['readonly'] = 'readonly'
       self.fields['requisition'].label = "Requisition No"
       # self.fields['item_name'].widget.attrs['value'] = self.instance.item_name
       # self.fields['item_name'].widget.attrs['readonly'] = 'readonly'
       # self.fields['item_name'].label = "Item Name"

       # self.fields['issued_by'].label = "Requisition Issued By"
       # self.fields['issued_by'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)


       # self.fields['department'].label = "Department"
       # self.fields['requisition_date'].label = "Requisition Date"
       # self.fields['quantity_requested'].label = "Requested Quantity"
       #self.fields['quantity_issued'].label = "Quantity Issued"
       #self.fields['quantity_issued'].widget.attrs['placeholder'] = "Enter Issue Quantity"
       # self.fields['requesting_staff'].label = "Requesting Staff"
       # self.fields['requesting_staff'].widget.attrs['placeholder'] = "Requesting Staff"
       # self.fields['issued_by'].label = "Issueing Officer"
       # self.fields['issued_by'].widget.attrs['placeholder'] = "Issuing Officer"

#RequisitionCartFormSet = modelformset_factory(RequisitionCart, form=RequisitionCartModelForm, can_delete=False, extra=0)  

IssueRequisitionItemFormSet = modelformset_factory(RequisitionCartItem, form=IssueRequisitionItemModelForm, can_delete=True, extra=0) 

# IssueRequisitionItemFormSet = modelformset_factory(
#     RequisitionItem, fields=('item', 'quantity', 'quantity_issued'), 
#     widgets={'quantity': forms.TextInput(attrs={'readonly': True})

#     },
#     can_delete=False, extra=0)


class RestockModelForm(forms.ModelForm):

    class Meta:
        model = Restock

        fields = ('restock_no', 'item_name', 'item_description', 'category', 'stock_code', 'vendor', 'unit', 'quantity_ordered', 'unit_price', 'quantity_received', 'received_by', 'received_on')

        widgets = {
       'item_description': forms.Textarea(attrs={'readonly': True,'rows':2, 'cols':12}),
       'restock_no': forms.HiddenInput(),
       'stock_code': forms.TextInput(attrs={'readonly': True}), 
       'item_name': forms.TextInput(attrs={'readonly': True}), 
       
       'unit': forms.TextInput(attrs={'readonly': True}), 

        }

        

    def __init__(self, *args, **kwargs):
       super(RestockModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
       
       self.fields['item_name'].label = "Item Name"
       self.fields['item_description'].label = "Item Description"
       self.fields['item_description'].widget.attrs['placeholder'] = "Enter Item Description"
       self.fields['category'].label = "Category"
       self.fields['stock_code'].label = "Stock Code"
       self.fields['vendor'].label = "Vendor"
       self.fields['unit'].label = "Unit of Measurement"
       self.fields['quantity_ordered'].label = "Quantity Ordered"
       self.fields['quantity_ordered'].widget.attrs['placeholder'] = "Enter Quantity Ordered"
       self.fields['unit_price'].label = "Unit Price"
       self.fields['unit_price'].widget.attrs['placeholder'] = "Enter Unit Price"
       self.fields['quantity_received'].label = "Quantity Received"
       self.fields['quantity_received'].widget.attrs['placeholder'] = "Enter Quantity Received"

    


