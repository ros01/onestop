from django import forms
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Category, Vendor, Contract, Project
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.utils import timezone
from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_modal_forms.mixins import PassRequestMixin, PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from tempus_dominus.widgets import DatePicker, DateTimePicker
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.models import ModelMultipleChoiceField
from django.forms import MultipleChoiceField
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()


class CategoryModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name', 'description', 'added_by')

        widgets = {
            'description': forms.Textarea(attrs={'rows':2, 'cols':3}),   
            }

                

    def __init__(self, *args, **kwargs):
       super(CategoryModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
       self.fields['category_name'].label = "Category Name"
       self.fields['category_name'].widget.attrs['placeholder'] = "Enter Category Name"
       self.fields['description'].label = "Description"
       self.fields['description'].widget.attrs['placeholder'] = "Enter Description"
             
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
        fields = ('vendor_name', 'description', 'address', 'phone', 'email', 'added_by')

        widgets = {
            'description': forms.Textarea(attrs={'rows':2, 'cols':3}),   
            }

    
    def __init__(self, *args, **kwargs):
       super(VendorModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
       self.fields['vendor_name'].label = "Vendor Name"
       self.fields['vendor_name'].widget.attrs['placeholder'] = "Enter Vendor Name"
       self.fields['description'].label = "Vendor Description"
       self.fields['description'].widget.attrs['placeholder'] = "Enter Vendor Description"
       self.fields['address'].label = "Address"
       self.fields['address'].widget.attrs['placeholder'] = "Enter Address"
       self.fields['phone'].label = "Phone"
       self.fields['phone'].widget.attrs['placeholder'] = "Enter Phone"
       self.fields['email'].label = "Email"
       self.fields['email'].widget.attrs['placeholder'] = "Enter Email"
             
    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance


class ContractModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    contact_award_date = forms.DateField(
      widget=DatePicker(
        options={

                'format': 'YYYY-MM-DD',
                'useCurrent': True,
                'collapse': False,
              },
        attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
                'sideBySide': True,
            }
            ),
      )

    projected_start_date = forms.DateField(
      widget=DatePicker(
        options={

                'format': 'YYYY-MM-DD',
                'useCurrent': True,
                'collapse': False,
              },
        attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
                'sideBySide': True,
            }
            ),
      )

    projected_end_date = forms.DateField(
      widget=DatePicker(
        options={

                'format': 'YYYY-MM-DD',
                'useCurrent': True,
                'collapse': False,
  
            },
        attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
                'sideBySide': True,
            }
            ),
      )
    
    class Meta:
        model = Contract
        fields = ('contract_no', 'contract_name', 'contract_description', 'category', 'vendor', 'contact_award_date', 'contact_award_amount', 'projected_start_date', 'projected_end_date', 'contract_award_letter', 'vendor_proposal', 'added_by')
        widgets = {
            'contract_description': forms.Textarea(attrs={'rows':2, 'cols':3}),
            'added_by': forms.HiddenInput(),   
            }

    def __init__(self, *args, **kwargs):
       super(ContractModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       
       self.fields['added_by'].initial = self.request.user
       self.fields['contract_name'].label = "Contract Name"
       self.fields['contract_name'].widget.attrs['placeholder'] = "Enter Contract Name"
       self.fields['category'].label = "Category"
       self.fields['category'].widget.attrs['placeholder'] = "Enter Category"
       self.fields['vendor'].label = "Vendor Name"
       self.fields['vendor'].widget.attrs['placeholder'] = "Enter Vendor Name"
       self.fields['contact_award_date'].label = "Contract Award Date"
       self.fields['contact_award_date'].widget.attrs['placeholder'] = "Enter Contract Award Date"
       self.fields['contact_award_amount'].label = "Contract Award Amount"
       self.fields['contact_award_amount'].widget.attrs['placeholder'] = "Enter Contract Award Amount"
       self.fields['contract_description'].label = "Contract Description"
       self.fields['contract_description'].widget.attrs['placeholder'] = "Enter Contract Description"
       self.fields['projected_start_date'].label = "Projected Start Date"
       self.fields['projected_start_date'].widget.attrs['placeholder'] = "Enter Projected Start Date"
       self.fields['projected_end_date'].label = "Projected End Date"
       self.fields['projected_end_date'].widget.attrs['placeholder'] = "Enter Projected End Date"
       self.fields['contract_award_letter'].label = "Contract Award Letter"
       self.fields['contract_award_letter'].widget.attrs['placeholder'] = "Enter Contract Award Letter"
       self.fields['vendor_proposal'].label = "Vendor Proposal"
       self.fields['vendor_proposal'].widget.attrs['placeholder'] = "Enter Vendor Proposal"
              

    def save(self):
      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)
      return instance


class ProjectModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    start_date = forms.DateField(
      widget=DatePicker(
        options={

                'format': 'YYYY-MM-DD',
                'useCurrent': True,
                'collapse': False,
              },
        attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
                'sideBySide': True,
            }
            ),
      )

    completion_date = forms.DateField(
      widget=DatePicker(
        options={

                'format': 'YYYY-MM-DD',
                'useCurrent': True,
                'collapse': False,
  
            },
        attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
                'sideBySide': True,
            }
            ),
      required=False
      )
    
    class Meta:
        model = Project
        fields = ('contract_no', 'contract_name', 'contract_description', 'category', 'vendor', 'contact_award_date', 'contact_award_amount', 'projected_start_date', 'projected_end_date', 'start_date', 'completion_date', 'contract_status', 'performance_rating', 'documented_by')
        widgets = {
        	#'documented_by': forms.HiddenInput(), 
            #'contract_description': forms.Textarea(attrs={'rows':2, 'cols':3}),
          'contract_description': forms.Textarea(attrs={'readonly': True,'rows':2, 'cols':12}),
          'contract_no': forms.TextInput(attrs={'readonly': True}), 
        	'contract_name': forms.TextInput(attrs={'readonly': True}),
        	'contact_award_date': forms.TextInput(attrs={'readonly': True}), 
        	'contact_award_amount': forms.TextInput(attrs={'readonly': True}),  
        	'projected_start_date': forms.TextInput(attrs={'readonly': True}),
        	'projected_end_date': forms.TextInput(attrs={'readonly': True}),         
        }

    def __init__(self, *args, **kwargs):
       super(ProjectModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       #self.fields['documented_by'].initial = self.request.user
       self.fields['contract_no'].label = "Contract No"
       self.fields['contract_name'].label = "Contract Name"
       self.fields['contract_name'].widget.attrs['placeholder'] = "Enter Contract Name"
       self.fields['contract_description'].label = "Contract Description"
       self.fields['contract_description'].widget.attrs['placeholder'] = "Enter Contract Description"
       self.fields['category'].label_from_instance = lambda obj: "{}".format(obj.category_name)
       self.fields['category'].widget.attrs['readonly'] = 'readonly'
       self.fields['category'].label = "Category"
       self.fields['vendor'].label_from_instance = lambda obj: "{}".format(obj.vendor_name)
       self.fields['vendor'].widget.attrs['readonly'] = 'readonly'
       self.fields['vendor'].label = "Vendor"
       self.fields['contact_award_date'].label = "Contract Award Date"
       self.fields['contact_award_date'].widget.attrs['placeholder'] = "Enter Contract Award Date"
       self.fields['contact_award_amount'].label = "Contract Amount"
       self.fields['contact_award_amount'].widget.attrs['placeholder'] = "Enter Contract Amount"
       self.fields['projected_start_date'].label = "Scheduled Start Date"
       self.fields['projected_end_date'].label = "Scheduled End Date"
       self.fields['start_date'].label = "Contract Start Date"
       self.fields['start_date'].widget.attrs['placeholder'] = "Select Contract Start Date"
       self.fields['completion_date'].label = "Completion Date"
       self.fields['completion_date'].widget.attrs['placeholder'] = "Select Completion Date"
       self.fields['contract_status'].label = "Contract Status"
       self.fields['contract_status'].widget.attrs['placeholder'] = "Contract Status"
       self.fields['performance_rating'].label = "Contract Rating"
       self.fields['performance_rating'].widget.attrs['placeholder'] = "Enter Contract Rating"
       
    def save(self):
      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)
      return instance


