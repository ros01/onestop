from django import forms
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Workshop, Station, Category, Vehicle, Assign, Release, Fueling, Repair, Schedule, Maintenance, Refill
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.utils import timezone
from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_modal_forms.mixins import PassRequestMixin, PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from tempus_dominus.widgets import DatePicker, DateTimePicker


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
        fields = ('station_name', 'contact_name', 'address', 'phone', 'email', 'station_credit', 're_order_credit', 'entered_by',)

                

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
       self.fields['station_credit'].label = "Station Credit"
       self.fields['station_credit'].widget.attrs['placeholder'] = "Enter Station Credit"
       self.fields['re_order_credit'].label = "Station Re-Order Credit"
       self.fields['re_order_credit'].widget.attrs['placeholder'] = "Enter Station Re-Order Credit"
       

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
        fields = ('vehicle_name', 'description', 'vehicle_type', 'model', 'purchase_year', 'location', 'category', 'engine_number', 'chasis_number', 'colour', 'department_assigned', 'private_license_no', 'official_license_no', 'insurance_details', 'entered_by',)

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
       self.fields['model'].label = "Model/Year of Manufacture"
       self.fields['model'].widget.attrs['placeholder'] = "Enter Year of Manufacture"
       self.fields['purchase_year'].label = "Year of Purchase"
       self.fields['purchase_year'].widget.attrs['placeholder'] = "Enter Year of Purchase"
       self.fields['location'].label = "Location"
       self.fields['engine_number'].label = "Engine Number"
       self.fields['engine_number'].widget.attrs['placeholder'] = "Enter Engine Number"
       self.fields['chasis_number'].label = "Chasis Number"
       self.fields['chasis_number'].widget.attrs['placeholder'] = "Enter Chasis Number"
       self.fields['colour'].label = "Vehicle Colour"
       self.fields['department_assigned'].label = "Department Assigned"
       self.fields['private_license_no'].label = "Private License Number"
       self.fields['private_license_no'].widget.attrs['placeholder'] = "Enter Private License Number"
       self.fields['official_license_no'].label = "Official License Number"
       self.fields['official_license_no'].widget.attrs['placeholder'] = "Enter Official License Number"
       self.fields['insurance_details'].label = "Insurance Certificate Number"
       self.fields['insurance_details'].widget.attrs['placeholder'] = "Enter Insurance Certificate Number"
       

    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance


class IssueVehicleRequestModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    approved_start_date = forms.DateTimeField(
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

    approved_end_date = forms.DateTimeField(
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
        model = Assign
        fields = ('request_no', 'vehicle_name', 'requesting_staff', 'department', 'request_reason', 'destination', 'request_date', 'driver', 'projected_start_date', 'projected_end_date', 'approved_start_date', 'approved_end_date','assigned_by')
        widgets = {
        'department': forms.HiddenInput(),
        'request_date': forms.HiddenInput(),   
        'requesting_staff': forms.HiddenInput(),
        'request_no': forms.TextInput(attrs={'readonly': True}), 
        'request_reason': forms.TextInput(attrs={'readonly': True}),
        'destination': forms.TextInput(attrs={'readonly': True}),
        'projected_start_date': forms.TextInput(attrs={'readonly': True}),
        'projected_end_date': forms.TextInput(attrs={'readonly': True}),
        }

    def __init__(self, *args, **kwargs):
       super(IssueVehicleRequestModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       self.fields['request_no'].label = "Request No"
       self.fields['vehicle_name'].widget.attrs['value'] = self.instance.vehicle_name
       self.fields['vehicle_name'].widget.attrs['readonly'] = 'readonly'
       self.fields['vehicle_name'].label = "Vehicle Name"
       self.fields['department'].label = "Department"
       self.fields['driver'].label = "Driver"
       self.fields['projected_start_date'].label = "Projected Start Date"
       self.fields['projected_end_date'].label = "Projected End Date"
       self.fields['approved_start_date'].label = "Approved Start Date"
       self.fields['approved_end_date'].label = "Approved End Date"
       self.fields['requesting_staff'].label = "Requesting Staff"
       self.fields['requesting_staff'].widget.attrs['placeholder'] = "Requesting Staff"
       self.fields['assigned_by'].label = "Issuing Officer"

    def save(self):
      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)
      return instance
       

class FinalizeTripModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    actual_trip_start_date = forms.DateTimeField(
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

    actual_trip_end_date = forms.DateTimeField(
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
        model = Release

        fields = ('request_no', 'vehicle_name', 'department', 'request_date', 'requesting_staff', 'driver', 'approved_start_date', 'approved_end_date', 'actual_trip_start_date', 'actual_trip_end_date', 'trip_start_mileage', 'trip_end_mileage', 'released_by')

        widgets = {
        'department': forms.HiddenInput(),
        'request_date': forms.HiddenInput(),   
        #'requesting_staff': forms.TextInput(attrs={'readonly': True}),
        #'vehicle': forms.TextInput(attrs={'readonly': True}),
        'request_no': forms.TextInput(attrs={'readonly': True}), 
        'driver': forms.TextInput(attrs={'readonly': True}),
        'approved_start_date': forms.TextInput(attrs={'readonly': True}),
        'approved_end_date': forms.TextInput(attrs={'readonly': True}),

        }

    def __init__(self, *args, **kwargs):
       super(FinalizeTripModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
      
       self.fields['request_no'].label = "Request No"
       #self.fields['vehicle'].label = "Vehicle ID"
       self.fields['vehicle_name'].widget.attrs['value'] = self.instance.vehicle_name
       self.fields['vehicle_name'].widget.attrs['readonly'] = 'readonly'
       self.fields['vehicle_name'].label = "Vehicle Name"
       self.fields['requesting_staff'].widget.attrs['readonly'] = 'readonly'
       self.fields['requesting_staff'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)
       self.fields['requesting_staff'].label = "Requesting Staff"
       self.fields['driver'].label = "Driver"
       self.fields['released_by'].label = "Released By:"
       self.fields['requesting_staff'].widget.attrs['placeholder'] = "Requesting Staff"
       self.fields['approved_start_date'].label = "Approved Start Date"
       self.fields['approved_end_date'].label = "Approved End Date"
       self.fields['actual_trip_start_date'].label = "Trip Start Date"
       self.fields['actual_trip_end_date'].label = "Trip End Date"
       self.fields['trip_start_mileage'].label = "Starting Mileage:"
       self.fields['trip_start_mileage'].widget.attrs['placeholder'] = "Enter Start Mileage"
       self.fields['trip_end_mileage'].label = "Mileage at Return:"
       self.fields['trip_end_mileage'].widget.attrs['placeholder'] = "Enter Mileage at Return"

    def save(self):
      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)
      return instance



       
class FuelingModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:
        model = Fueling
        fields = ('vehicle', 'driver', 'voucher_no', 'current_mileage', 'fuel_input', 'fuel_cost', 'station', 'authorised_by')

                

    def __init__(self, *args, **kwargs):
       super(FuelingModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
       self.fields['vehicle'].label = "Vehicle Name"
       self.fields['station'].label = "Station Name"
       self.fields['driver'].label = "Driver Name"
       self.fields['driver'].widget.attrs['placeholder'] = "Enter Driver Name"
       self.fields['voucher_no'].label = "Voucher Number"
       self.fields['voucher_no'].widget.attrs['placeholder'] = "Enter Voucher Number"
       self.fields['current_mileage'].label = "Current Mileage"
       self.fields['current_mileage'].widget.attrs['placeholder'] = "Enter Current Mileage"
       self.fields['fuel_input'].label = "Fuel Quantity"
       self.fields['fuel_input'].widget.attrs['placeholder'] = "Enter Fuel Quantity"
       self.fields['fuel_cost'].label = "Fuel Cost"
       self.fields['fuel_cost'].widget.attrs['placeholder'] = "Enter Fuel Cost"
       self.fields['authorised_by'].label = "Authorized By"
      
       

    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance


class RepairsModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:
        model = Repair  
        fields = ('vehicle', 'fault', 'driver', 'reported_by', 'current_mileage', 'repair_details', 'repair_cost', 'workshop', 'mechanic_name', 'authorised_by') 

        widgets = {
            'fault': forms.Textarea(attrs={'rows':2, 'cols':3}), 
            'repair_details': forms.Textarea(attrs={'rows':2, 'cols':3}),  
            }

          

    def __init__(self, *args, **kwargs):
       super(RepairsModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
       self.fields['vehicle'].label = "Vehicle Name"
       self.fields['workshop'].label = "Workshop Name" 
       self.fields['mechanic_name'].label = "Mechanic Name"
       self.fields['driver'].label = "Driver Name"
       self.fields['driver'].widget.attrs['placeholder'] = "Enter Driver Name"
       self.fields['fault'].label = "Fault Details"
       self.fields['fault'].widget.attrs['placeholder'] = "Enter Fault Details"
       self.fields['current_mileage'].label = "Current Mileage"
       self.fields['current_mileage'].widget.attrs['placeholder'] = "Enter Current Mileage"
       self.fields['repair_details'].label = "Repair Details"
       self.fields['repair_details'].widget.attrs['placeholder'] = "Enter Repair Details"
       self.fields['repair_cost'].label = "Repair Cost"
       self.fields['repair_cost'].widget.attrs['placeholder'] = "Enter Repair Cost"
    
    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance


class ScheduleModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    target_maintenance_date = forms.DateTimeField(
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
        model = Schedule
        fields = ('schedule_no', 'vehicle', 'target_maintenance_mileage', 'target_maintenance_date', 'maintenance_scheduled_by')
        widgets = {
            
            'schedule_no': forms.HiddenInput(),
            
          
            }

    def __init__(self, *args, **kwargs):
       super(ScheduleModelForm, self).__init__(*args, **kwargs)
       self.fields['vehicle'].label = "Vehicle Name"
       #self.fields['workshop'].label = "Workshop Name"
       #self.fields['mechanic_name'].label = "Mechanic Name"
       self.fields['target_maintenance_mileage'].label = "Target Maintenance Mileage"
       self.fields['target_maintenance_mileage'].widget.attrs['placeholder'] = "Enter Target Maintenance Mileage"
       self.fields['target_maintenance_date'].label = "Target Maintenance Date"
       #self.fields['driver'].label = "Driver Name"
       #self.fields['driver'].widget.attrs['placeholder'] = "Enter Driver Name"
       #self.fields['last_maintenance_date'].label = "Last Maintenance Date"   
       #self.fields['maintenance_cost_estimate'].label = "Maintenance Estimate"
       #self.fields['maintenance_cost_estimate'].widget.attrs['placeholder'] = "Enter Maintenance Estimate"
       #self.fields['projected_maintenance'].label = "Projected Maintenance"
       #self.fields['projected_maintenance'].widget.attrs['placeholder'] = "Enter Projected Maintenance"

    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance
      


#class RecordMaintenanceModelForm(forms.ModelForm):
 
    #class Meta:
        #model = Maintenance

        #fields = ('schedule_no', 'vehicle', 'driver', 'target_maintenance_date', 'workshop', 'mechanic_name', 'maintenance_scheduled_by', 'scheduled_on', 'current_maintenance_mileage', 'actual_maintenance_cost', 'actual_maintenance_details', 'next_maintenance_date', 'maintenance_recorded_by', 'actual_maintenance_date')

        #widgets = {
        #'maintenance_scheduled_by': forms.HiddenInput(),
        #'scheduled_on': forms.HiddenInput(),
        #'schedule_no': forms.TextInput(attrs={'readonly': True}), 
        #'target_maintenance_date':forms.TextInput(attrs={'readonly': True}),
        #'actual_maintenance_details': forms.Textarea(attrs={'rows':2, 'cols':3}), 
        #}

    #def __init__(self, *args, **kwargs):
       #super(RecordMaintenanceModelForm, self).__init__(*args, **kwargs)
       #for name in self.fields.keys():
            #elf.fields[name].widget.attrs.update({
                #'class': 'form-control',
           # })
      
      
       #self.fields['schedule_no'].label = "Schedule No"
       #self.fields['vehicle'].widget.attrs['value'] = self.instance.vehicle
       #self.fields['vehicle'].widget.attrs['readonly'] = 'readonly'
       #self.fields['vehicle'].label = "Vehicle Name"
       #self.fields['driver'].label = "Driver"
       #self.fields['driver'].widget.attrs['placeholder'] = "Enter Driver Name"
       #self.fields['target_maintenance_date'].label = "Target Maintenance Date"
       #self.fields['next_maintenance_date'].label = "Next Maintenance Date"
       #self.fields['actual_maintenance_date'].label = "Actual Maintenance Date"
       #self.fields['workshop'].label = "Workshop"
       #self.fields['mechanic_name'].label = "Mechanic Name"
       #self.fields['current_maintenance_mileage'].label = "Current Mileage:"
       #self.fields['current_maintenance_mileage'].widget.attrs['placeholder'] = "Enter Mileage at Maintenance"
       #self.fields['actual_maintenance_cost'].label = "Actual Maintenance Cost:"
       #self.fields['actual_maintenance_cost'].widget.attrs['placeholder'] = "Enter Actual Cost of Maintenance"
       #self.fields['actual_maintenance_details'].label = "Actual Maintenance Details:"
       #self.fields['actual_maintenance_details'].widget.attrs['placeholder'] = "Enter Actual Maintenance Details"
      

 

class RecordMaintenanceModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    maintenance_date = forms.DateTimeField(
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
        model = Maintenance
        fields = ('schedule_no', 'vehicle', 'driver', 'target_maintenance_date', 'target_maintenance_mileage', 'workshop', 'mechanic_name', 'maintenance_scheduled_by', 'scheduled_on', 'current_mileage', 'maintenance_cost', 'maintenance_details', 'maintenance_recorded_by', 'maintenance_date')
        widgets = {
        'maintenance_scheduled_by': forms.HiddenInput(),
        'scheduled_on': forms.HiddenInput(),
        'schedule_no': forms.TextInput(attrs={'readonly': True}), 
        'target_maintenance_date':forms.TextInput(attrs={'readonly': True}),
        'target_maintenance_mileage':forms.TextInput(attrs={'readonly': True}),
        'maintenance_details': forms.Textarea(attrs={'rows':2, 'cols':3}), 
        }

    def __init__(self, *args, **kwargs):
       super(RecordMaintenanceModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       self.fields['schedule_no'].label = "Schedule No"
       self.fields['vehicle'].widget.attrs['value'] = self.instance.vehicle
       self.fields['vehicle'].widget.attrs['readonly'] = 'readonly'
       self.fields['vehicle'].label = "Vehicle Name"
       self.fields['driver'].label = "Driver"
       self.fields['driver'].widget.attrs['placeholder'] = "Enter Driver Name"
       self.fields['target_maintenance_date'].label = "Target Maintenance Date"
       self.fields['maintenance_date'].label = "Maintenance Date"
       self.fields['workshop'].label = "Workshop"
       self.fields['mechanic_name'].label = "Mechanic Name"
       self.fields['current_mileage'].label = "Current Mileage:"
       self.fields['current_mileage'].widget.attrs['placeholder'] = "Enter Mileage at Maintenance"
       self.fields['maintenance_cost'].label = "Maintenance Cost:"
       self.fields['maintenance_cost'].widget.attrs['placeholder'] = "Enter Cost of Maintenance"
       self.fields['maintenance_details'].label = "Maintenance Details:"
       self.fields['maintenance_details'].widget.attrs['placeholder'] = "Enter Maintenance Details"

    def save(self):
      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)
      return instance   

    

        

class RefillModelForm(forms.ModelForm):

    class Meta:
        model = Refill

        fields = ('refill_no', 'station_name', 'address', 'phone', 'email', 'station_credit', 'refill_credit_value', 'refill_by')

        widgets = {
       'station_name': forms.TextInput(attrs={'readonly': True}),
       'phone': forms.TextInput(attrs={'readonly': True}),
       'address': forms.Textarea(attrs={'readonly': True,'rows':2, 'cols':12}),
       'refill_no': forms.HiddenInput(),
       'email': forms.HiddenInput(),
       'station_credit': forms.TextInput(attrs={'readonly': True}),

        }

        

    def __init__(self, *args, **kwargs):
       super(RefillModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
       
       self.fields['station_name'].label = "Station Name"
       self.fields['address'].label = "Station Address"
       self.fields['address'].widget.attrs['placeholder'] = "Enter Station Address"
       self.fields['phone'].label = "Phone"
       self.fields['email'].label = "Email"
       self.fields['refill_credit_value'].label = "Restock Credit Value"
       self.fields['refill_credit_value'].widget.attrs['placeholder'] = "Enter Restock Credit Value"
       




