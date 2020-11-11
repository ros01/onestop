from django import forms
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Workshop, Station, Category, Vehicle, Assign, Release, Fueling, Repair, Schedule, Maintenance
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.utils import timezone
from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_modal_forms.mixins import PassRequestMixin, PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from tempus_dominus.widgets import DatePicker

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
        fields = ('station_name', 'contact_name', 'address', 'phone', 'email', 'station_credit', 'entered_by',)

                

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
        fields = ('vehicle_name', 'description', 'vehicle_type', 'model', 'purchase_year', 'location', 'category', 'engine_number', 'chasis_number', 'colour', 'department_assigned', 'license_no', 'insurance_details', 'entered_by',)

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
       

class FinalizeTripModelForm(forms.ModelForm):
 
    class Meta:
        model = Release

        fields = ('request_no', 'vehicle', 'department', 'request_date', 'requesting_staff', 'driver', 'start_date', 'end_date', 'trip_start_mileage', 'trip_end_mileage', 'released_by')

        widgets = {
        'department': forms.HiddenInput(),
        'request_date': forms.HiddenInput(),   
        'requesting_staff': forms.TextInput(attrs={'readonly': True}),
        'vehicle': forms.TextInput(attrs={'readonly': True}),
        'request_no': forms.TextInput(attrs={'readonly': True}), 
        'driver': forms.TextInput(attrs={'readonly': True}),
        'start_date': DatePickerInput(format='%Y-%m-%d'),
        'end_date': DatePickerInput(format='%Y-%m-%d'), 

        }

    def __init__(self, *args, **kwargs):
       super(FinalizeTripModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
      
       self.fields['request_no'].label = "Request No"
       self.fields['vehicle'].label = "Vehicle ID"
       self.fields['driver'].label = "Driver"
       self.fields['start_date'].label = "Trip Start Date"
       self.fields['end_date'].label = "Trip End Date"
       self.fields['requesting_staff'].label = "Requesting Staff"
       self.fields['released_by'].label = "Released By:"
       self.fields['requesting_staff'].widget.attrs['placeholder'] = "Requesting Staff"
       self.fields['trip_start_mileage'].label = "Starting Mileage:"
       self.fields['trip_start_mileage'].widget.attrs['placeholder'] = "Enter Start Mileage"
       self.fields['trip_end_mileage'].label = "Mileage at Return:"
       self.fields['trip_end_mileage'].widget.attrs['placeholder'] = "Enter Mileage at Return"



       
class FuelingModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:
        model = Fueling
        fields = ('vehicle', 'driver', 'current_mileage', 'fuel_input', 'fuel_cost', 'station', 'authorised_by')

                

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
          instance.save()
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


class ScheduleModelForm(forms.ModelForm):
    

    class Meta:
        model = Schedule
        fields = ('schedule_no', 'vehicle', 'current_mileage', 'maintenance_due_date', 'workshop', 'mechanic_name', 'maintenance_scheduled_by')
        widgets = {
            #'projected_maintenance': forms.Textarea(attrs={'rows':2, 'cols':3}), 
            'schedule_no': forms.HiddenInput(),
            #'last_maintenance_date': DateTimePickerInput(),
            'maintenance_due_date': DateTimePickerInput(),
          
            }

    def __init__(self, *args, **kwargs):
       super(ScheduleModelForm, self).__init__(*args, **kwargs)
       self.fields['vehicle'].label = "Vehicle Name"
       self.fields['workshop'].label = "Workshop Name"
       self.fields['mechanic_name'].label = "Mechanic Name"
       #self.fields['driver'].label = "Driver Name"
       #self.fields['driver'].widget.attrs['placeholder'] = "Enter Driver Name"
       self.fields['current_mileage'].label = "Current Mileage"
       self.fields['current_mileage'].widget.attrs['placeholder'] = "Enter Current Mileage"
       #self.fields['last_maintenance_date'].label = "Last Maintenance Date"
       self.fields['maintenance_due_date'].label = "Maintenance Due Date"
       #self.fields['maintenance_cost_estimate'].label = "Maintenance Estimate"
       #self.fields['maintenance_cost_estimate'].widget.attrs['placeholder'] = "Enter Maintenance Estimate"
       #self.fields['projected_maintenance'].label = "Projected Maintenance"
       #self.fields['projected_maintenance'].widget.attrs['placeholder'] = "Enter Projected Maintenance"

    
      


class RecordMaintenanceModelForm(forms.ModelForm):
 
    class Meta:
        model = Maintenance

        fields = ('schedule_no', 'vehicle', 'driver', 'maintenance_due_date', 'workshop', 'mechanic_name', 'maintenance_scheduled_by', 'scheduled_on', 'current_maintenance_mileage', 'actual_maintenance_cost', 'actual_maintenance_details', 'next_maintenance_date', 'maintenance_recorded_by', 'actual_maintenance_date')

        widgets = {
        #'department': forms.HiddenInput(),
        #'request_date': forms.HiddenInput(),   
        #'requesting_staff': forms.HiddenInput(),
        
        #'driver': forms.HiddenInput(),
        'maintenance_scheduled_by': forms.HiddenInput(),
        'scheduled_on': forms.HiddenInput(),
        'schedule_no': forms.TextInput(attrs={'readonly': True}), 
        'vehicle': forms.TextInput(attrs={'readonly': True}),
        #'last_maintenance_mileage': forms.TextInput(attrs={'readonly': True}),
        #'last_maintenance_date': forms.TextInput(attrs={'readonly': True}),
        'maintenance_due_date':forms.TextInput(attrs={'readonly': True}),
        #'maintenance_cost_estimate': forms.TextInput(attrs={'readonly': True}),
        #'projected_maintenance': forms.Textarea(attrs={'readonly': True,'rows':2, 'cols':3}),
        'actual_maintenance_details': forms.Textarea(attrs={'rows':2, 'cols':3}), 
        'next_maintenance_date': DateTimePickerInput(),
        'actual_maintenance_date': DateTimePickerInput(),


        }

    def __init__(self, *args, **kwargs):
       super(RecordMaintenanceModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
      
       self.fields['schedule_no'].label = "Schedule No"
       self.fields['vehicle'].label = "Vehicle ID"
       self.fields['driver'].label = "Driver"
       #self.fields['last_maintenance_mileage'].label = "Mileage at Last Maintenance"
       #self.fields['last_maintenance_date'].label = "Last Maintenance Date"
       self.fields['maintenance_due_date'].label = "Maintenance Due Date"
       self.fields['next_maintenance_date'].label = "Next Maintenance Date"
       self.fields['actual_maintenance_date'].label = "Actual Maintenance Date"
       self.fields['workshop'].label = "Workshop"
       self.fields['mechanic_name'].label = "Mechanic Name"
       #self.fields['maintenance_cost_estimate'].label = "Estimated Cost of Maintenance"
       #self.fields['projected_maintenance'].label = "Projected Maintenance Details"
       #self.fields['maintenance_scheduled_by'].label = "Maintenance Scheduled By:"
       #self.fields['scheduled_on'].label = "Maintenance Schedule Created On:"
       self.fields['current_maintenance_mileage'].label = "Current Mileage:"
       self.fields['current_maintenance_mileage'].widget.attrs['placeholder'] = "Enter Mileage at Maintenance"
       self.fields['actual_maintenance_cost'].label = "Actual Maintenance Cost:"
       self.fields['actual_maintenance_cost'].widget.attrs['placeholder'] = "Enter Actual Cost of Maintenance"
       self.fields['actual_maintenance_details'].label = "Actual Maintenance Details:"
       self.fields['actual_maintenance_details'].widget.attrs['placeholder'] = "Enter Actual Maintenance Details"
       #self.fields['maintenance_recorded_by'].label = "Maintenance Recorded By:"

    

        






