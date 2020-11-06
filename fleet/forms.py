from django import forms
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Workshop, Station, Category, Vehicle, Assign
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.utils import timezone
from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_modal_forms.mixins import PassRequestMixin, PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_datepicker_plus import DatePickerInput

class WorkshopModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:
        model = Workshop
        fields = ('workshop_name', 'mechanic_name', 'address', 'phone', 'email', 'entered_by',)

                

    def __init__(self, *args, **kwargs):
       super(WorkshopModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
       self.fields['workshop_name'].label = "Workshop Name"
       self.fields['workshop_name'].widget.attrs['placeholder'] = "Workshop Name"
       self.fields['mechanic_name'].label = "Mechanic Name"
       self.fields['mechanic_name'].widget.attrs['placeholder'] = "Mechanic Name"
       self.fields['address'].label = "Address"
       self.fields['address'].widget.attrs['placeholder'] = "Workshop Address"
       self.fields['phone'].label = "Phone"
       self.fields['phone'].widget.attrs['placeholder'] = "Phone"
       self.fields['email'].label = "Email"
       self.fields['email'].widget.attrs['placeholder'] = "Email"
       

    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance


class StationModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:
        model = Station
        fields = ('station_name', 'contact_name', 'address', 'phone', 'email', 'entered_by',)

                

    def __init__(self, *args, **kwargs):
       super(StationModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
       self.fields['station_name'].label = "Station Name"
       self.fields['station_name'].widget.attrs['placeholder'] = "Station Name"
       self.fields['contact_name'].label = "Contact Name"
       self.fields['contact_name'].widget.attrs['placeholder'] = "Contact Name"
       self.fields['address'].label = "Address"
       self.fields['address'].widget.attrs['placeholder'] = "Station Address"
       self.fields['phone'].label = "Phone"
       self.fields['phone'].widget.attrs['placeholder'] = "Phone"
       self.fields['email'].label = "Email"
       self.fields['email'].widget.attrs['placeholder'] = "Email"
       

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
        fields = ('category_name', 'description', 'entered_by',)

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
       self.fields['category_name'].widget.attrs['placeholder'] = "Category Name"
       self.fields['description'].label = "Description"
       self.fields['description'].widget.attrs['placeholder'] = "Description"
       

    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance

  
  

class VehicleModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:
        model = Vehicle
        fields = ('vehicle_name', 'description', 'vehicle_type', 'category', 'engine_number', 'chasis_number', 'colour', 'department_assigned', 'license_no', 'insurance_details', 'entered_by',)

        widgets = {
            'description': forms.Textarea(attrs={'rows':2, 'cols':3}),   
            }

                

    def __init__(self, *args, **kwargs):
       super(VehicleModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
       self.fields['vehicle_name'].label = "Vehicle Name"
       self.fields['vehicle_name'].widget.attrs['placeholder'] = "Vehicle Name"
       self.fields['description'].label = "Vehicle Description"
       self.fields['description'].widget.attrs['placeholder'] = "Vehicle Description"
       self.fields['vehicle_type'].label = "Vehicle Type"
       self.fields['category'].label = "Vehicle Category"
       self.fields['engine_number'].label = "Engine Number"
       self.fields['engine_number'].widget.attrs['placeholder'] = "Enter Engine Number"
       self.fields['chasis_number'].label = "Chasis Number"
       self.fields['chasis_number'].widget.attrs['placeholder'] = "Enter Chasis Number"
       self.fields['colour'].label = "Vehicle Colour"
       self.fields['department_assigned'].label = "Department Assigned"
       self.fields['license_no'].label = "License Number"
       self.fields['license_no'].widget.attrs['placeholder'] = "Enter License Number"
       self.fields['insurance_details'].label = "Insurance Certificate Number"
       self.fields['insurance_details'].widget.attrs['placeholder'] = "Enter Insurance Certificate Number"
       

    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance


class IssueVehicleRequestModelForm(forms.ModelForm):
 
    class Meta:
        model = Assign

        fields = ('request_no', 'vehicle', 'department', 'request_date', 'request_reason','destination', 'requesting_staff', 'driver', 'current_mileage', 'start_date', 'end_date','assigned_by')

        widgets = {
        'department': forms.HiddenInput(),
        'request_date': forms.HiddenInput(),   
        'requesting_staff': forms.HiddenInput(),
        'vehicle': forms.TextInput(attrs={'readonly': True}),
        'request_no': forms.TextInput(attrs={'readonly': True}), 
        'request_reason': forms.TextInput(attrs={'readonly': True}),
        'destination': forms.TextInput(attrs={'readonly': True}),
        'start_date': DatePickerInput(format='%Y-%m-%d'),
        'end_date': DatePickerInput(format='%Y-%m-%d'), 

        }

    def __init__(self, *args, **kwargs):
       super(IssueVehicleRequestModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
      
       self.fields['request_no'].label = "Request No"
       self.fields['vehicle'].label = "Vehicle ID"
       self.fields['department'].label = "Department"
       self.fields['driver'].label = "Driver"
       self.fields['start_date'].label = "Trip Start Date"
       self.fields['end_date'].label = "Trip End Date"
       self.fields['requesting_staff'].label = "Requesting Staff"
       self.fields['requesting_staff'].widget.attrs['placeholder'] = "Requesting Staff"
       self.fields['assigned_by'].label = "Issuing Officer"
       







