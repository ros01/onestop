from django import forms
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Request
from store.models import Requisition 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.utils import timezone
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PassRequestMixin, PopRequestMixin, CreateUpdateAjaxMixin
from fleet.models import Vehicle
from hr.models import Employee, Leave
from tempus_dominus.widgets import DatePicker, DateTimePicker


class RequisitionModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Requisition
        fields = ('employee', 'requisition_cart', 'requisition_reason', 'hod','department')
        widgets = {
        'requisition_cart': forms.HiddenInput(),
        'employee': forms.HiddenInput(),
        'department': forms.HiddenInput(),
        #'department': forms.TextInput(attrs={'readonly': True}), 
        #'item': forms.TextInput(attrs={'readonly': True}), 
        }

    def __init__(self, *args, **kwargs):
       super(RequisitionModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      # self.fields['item'].label = "Item Name"
       #self.fields['quantity_requested'].label = "Quantity Requested"
       self.fields['employee'].label = "Requesting Staff"
       self.fields['department'].label = "Department"

    def save(self):
      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)
      return instance




class OrderModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    projected_start_date = forms.DateTimeField(
      widget=DateTimePicker(
        options={

                'format': 'YYYY-MM-DD HH:mm',
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
    
    projected_end_date = forms.DateTimeField(
      widget=DateTimePicker(
        options={
                'format': 'YYYY-MM-DD HH:mm',
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
        model = Request
        fields = ('request_no', 'vehicle_name', 'department', 'request_reason', 'destination', 'request_duration', 'projected_start_date', 'projected_end_date', 'requesting_staff', )
        widgets = {
        'request_no': forms.HiddenInput(),
        'requesting_staff': forms.HiddenInput(),
        'request_reason': forms.Textarea(attrs={'rows':2, 'cols':3}),
        'department': forms.HiddenInput(),
        'vehicle_name': forms.TextInput(attrs={'readonly': True}),  
        }

    def __init__(self, *args, **kwargs):
       super(OrderModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       self.fields['vehicle_name'].label = "Vehicle"
       self.fields['request_reason'].label = "Request Reason"
       self.fields['request_reason'].widget.attrs['placeholder'] = "Enter reason for vehicle request"
       self.fields['destination'].label = "Destination"
       self.fields['destination'].widget.attrs['placeholder'] = "Enter Destination"
       self.fields['request_duration'].label = "Trip Duration"
       self.fields['request_duration'].widget.attrs['placeholder'] = "Enter Duration of Trip"
       self.fields['projected_start_date'].label = "Projected Start Date"
       self.fields['projected_end_date'].label = "Projected End Date"
       self.fields['department'].label = "Department"

    def save(self):
      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)
      return instance


LOCATION_CHOICES = (
  ('HQ', 'HQ'),
  ('Lagos Zonal Office ', 'Lagos Zonal Office'),
  ('Lagos CERT-RADMIRS', 'Lagos CERT-RADMIRS'),
  ('Asaba', 'Asaba'),
  ('Enugu', 'Enugu'),
  ('Port Harcourt', 'Port Harcourt'),
  ('Kano', 'Kano'),
  ('Sokoto', 'Sokoto'),
  ('Nnewi', 'Nnewi'),
  ('Calabar', 'Calabar'),
)


TRIP_CHOICES = (
  ('local', 'Local Trip'),
  ('interstate', 'Interstate Trip'),
)


#class VehicleFilterForm(forms.Form):
  #location = forms.ChoiceField(
    #label='Location',
    #choices=LOCATION_CHOICES, 
    #widget=forms.CheckboxSelectMultiple, 
    #required=False)
  
  #trip_type = forms.ChoiceField(
    #label='Trip Type',
    #choices=TRIP_CHOICES, 
    #widget=forms.CheckboxSelectMultiple, 
    #required=False)   



class VehicleFilterForm(forms.ModelForm):
    location = forms.ChoiceField(choices = LOCATION_CHOICES, widget=forms.Select(), required=True)
    trip_type = forms.ChoiceField(choices = TRIP_CHOICES, widget=forms.Select(), required=True)


    class Meta:
        model = Vehicle
        fields = ('location', 'trip_type')



    def __init__(self, *args, **kwargs):
       super(VehicleFilterForm, self).__init__(*args, **kwargs)
       self.fields['location'].label = "Location"
       self.fields['trip_type'].label = "Trip Type"
       


class StaffProfileModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    dob = forms.DateField(
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

    date_joined = forms.DateField(
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


    pension_date = forms.DateField(
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
        model = Employee
        fields = ('employee', 'dob', 'gender', 'marital_status', 'next_of_kin', 'nationality', 'email', 'phone', 'zone', 'department', 'designation', 'pay_grade', 'national_id', 'staff_id', 'national_id', 'contact_address', 'city', 'state', 'state_of_origin', 'local_government_area', 'state', 'date_joined', 'pension_date', 'qualification', 'languages', 'professional_organizations', 'blood_group', 'drivers_license', 'digital_passport', 'special_interests', 'hobbies')
        
        widgets = {
            #'staff_name': forms.TextInput(attrs={'readonly': True}),
            #'department': forms.TextInput(attrs={'readonly': True}),
            'email': forms.TextInput(attrs={'readonly': True}),
            'phone': forms.TextInput(attrs={'readonly': True}),
            'contact_address': forms.Textarea(attrs={'rows':2, 'cols':3}), 
            'hobbies': forms.Textarea(attrs={'rows':2, 'cols':3}),
            'special_interests': forms.Textarea(attrs={'rows':2, 'cols':3}),  
            }            

    def __init__(self, *args, **kwargs):
       super(StaffProfileModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

       self.fields['employee'].initial = self.request.user.id
       self.fields['employee'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)
       self.fields['employee'].label = "Staff Name"
       self.fields['employee'].widget.attrs['readonly'] = 'readonly'
       #self.fields['department'].initial = self.request.user.department
       self.fields['email'].initial = self.request.user.email
       self.fields['phone'].initial = self.request.user.phone_no
       self.fields['dob'].label = "Date of Birth"
       self.fields['dob'].widget.attrs['placeholder'] = "Enter Date of Birth"
       self.fields['next_of_kin'].label = "Next of Kin"
       self.fields['next_of_kin'].widget.attrs['placeholder'] = "Enter Next of Kin"
       self.fields['nationality'].label = "Nationality"
       self.fields['nationality'].widget.attrs['placeholder'] = "Enter Nationality"
       self.fields['email'].label = "Email"
       self.fields['email'].widget.attrs['placeholder'] = "Enter Email"
       self.fields['phone'].label = "Phone"
       self.fields['phone'].widget.attrs['placeholder'] = "Enter Phone"
       self.fields['zone'].label = "Location"
       self.fields['zone'].widget.attrs['placeholder'] = "Enter Location"
       self.fields['department'].label = "Department"
       self.fields['department'].widget.attrs['placeholder'] = "Enter Department"
       self.fields['designation'].label = "Designation"
       self.fields['designation'].widget.attrs['placeholder'] = "Enter Designation"
       self.fields['pay_grade'].label = "Pay Grade"
       self.fields['pay_grade'].widget.attrs['placeholder'] = "Enter Pay Grade"
       self.fields['national_id'].label = "National ID"
       self.fields['national_id'].widget.attrs['placeholder'] = "Enter National ID"
       self.fields['staff_id'].label = "Employee ID"
       self.fields['staff_id'].widget.attrs['placeholder'] = "Enter Employee ID"
       self.fields['contact_address'].label = "Contact Address"
       self.fields['contact_address'].widget.attrs['placeholder'] = "Enter Contact Address"
       self.fields['city'].label = "City"
       self.fields['city'].widget.attrs['placeholder'] = "Enter City"
       self.fields['state'].label = "State"
       self.fields['state'].widget.attrs['placeholder'] = "Enter State"
       self.fields['state_of_origin'].label = "State of Origin"
       self.fields['state_of_origin'].widget.attrs['placeholder'] = "Enter State of Origin"
       self.fields['local_government_area'].label = "Local Government Area"
       self.fields['local_government_area'].widget.attrs['placeholder'] = "Enter Local Government Area"
       self.fields['state'].label = "State"
       self.fields['state'].widget.attrs['placeholder'] = "Enter State"
       self.fields['date_joined'].label = "Service Start Date"
       self.fields['date_joined'].widget.attrs['placeholder'] = "Enter Service Start Date"
       self.fields['pension_date'].label = "Pension Start Date"
       self.fields['pension_date'].widget.attrs['placeholder'] = "Enter Pension Start Date"
       self.fields['qualification'].label = "Qualification"
       self.fields['qualification'].widget.attrs['placeholder'] = "Enter Qualification"
       self.fields['languages'].label = "Languages"
       self.fields['languages'].widget.attrs['placeholder'] = "Enter Languages"
       self.fields['professional_organizations'].label = "Professional Bodies"
       self.fields['professional_organizations'].widget.attrs['placeholder'] = "Enter Professional Bodies"
       self.fields['blood_group'].label = "Blood Group"
       self.fields['blood_group'].widget.attrs['placeholder'] = "Enter Blood Group"
       self.fields['drivers_license'].label = "Drivers License"
       self.fields['drivers_license'].widget.attrs['placeholder'] = "Enter Drivers License"
       self.fields['digital_passport'].label = "Digital Passport"
       self.fields['digital_passport'].widget.attrs['placeholder'] = "Upload Digital Passport"
       self.fields['special_interests'].label = "Special Interests"
       self.fields['special_interests'].widget.attrs['placeholder'] = "Enter Special Interests"
       self.fields['hobbies'].label = "Hobbies"
       self.fields['hobbies'].widget.attrs['placeholder'] = "Enter Hobbies"
           
    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance




class LeaveRequestModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    requested_start_date = forms.DateField(
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

    requested_end_date = forms.DateField(
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
        model = Leave
        fields = ('staff_name', 'requested_start_date', 'requested_end_date', 'leave_type')
            
    def __init__(self, *args, **kwargs):
       super(LeaveRequestModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       self.fields['requested_start_date'].label = "Requested Start Date"
       self.fields['requested_start_date'].widget.attrs['placeholder'] = "Enter Requested Start Date"
       self.fields['requested_end_date'].label = "Requested End Date"
       self.fields['requested_end_date'].widget.attrs['placeholder'] = "Enter Requested End Date"
       self.fields['leave_type'].label = "Leave Type"
       self.fields['leave_type'].widget.attrs['placeholder'] = "Enter Leave Type"
       
           
    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance








       