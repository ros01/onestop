from django import forms
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Requisition, Request
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.utils import timezone
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PassRequestMixin, PopRequestMixin, CreateUpdateAjaxMixin
from fleet.models import Vehicle


class RequisitionModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:
        model = Requisition
        fields = ('requisition_no', 'item', 'quantity_requested', 'requesting_staff', 'department')


        widgets = {
        'requisition_no': forms.HiddenInput(),
        'requesting_staff': forms.HiddenInput(),
        'department': forms.TextInput(attrs={'readonly': True}),
        
        }

    def __init__(self, *args, **kwargs):
       super(RequisitionModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       
       self.fields['item'].label = "Item"
       self.fields['quantity_requested'].label = "Quantity Requested"
       self.fields['requesting_staff'].label = "Requesting Staff"
       self.fields['department'].label = "Department"

    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance











class RequestModelForm(forms.ModelForm):

    class Meta:
        model = Request
        fields = ('request_no', 'vehicle_name', 'department', 'request_reason', 'destination', 'request_duration', 'requesting_staff', )


        widgets = {
        'request_no': forms.HiddenInput(),
        'requesting_staff': forms.HiddenInput(),
        'request_reason': forms.Textarea(attrs={'rows':2, 'cols':3}),
        'department': forms.HiddenInput(),
        'vehicle_name': forms.TextInput(attrs={'readonly': True}),
        
        }

    def __init__(self, *args, **kwargs):
       super(RequestModelForm, self).__init__(*args, **kwargs)
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
       self.fields['department'].label = "Department"

    #def save(self):

      #if not self.request.is_ajax():
          #instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          #instance.save()
      #else:
          #instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      #return instance





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
  ('short', 'Short Trip'),
  ('long', 'Long Trip'),
)


class VehicleFilterForm(forms.ModelForm):
    #q = forms.CharField(label='Search', required=False)
    #vehicle_name = forms.ModelMultipleChoiceField(
      #label='Vehicle',
      #queryset=Vehicle.objects.all(), 
      #widget=forms.CheckboxSelectMultiple, 

    class Meta:
        fields = ('location', 'trip_type',)

    location = forms.ChoiceField(choices=LOCATION_CHOICES)

    trip_type = forms.ChoiceField(choices=TRIP_CHOICES)

    def __init__(self, *args, **kwargs):
       super(VehicleFilterForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
            self.fields[name].empty_label = None
       
       self.fields['location'].label = "Location"
       self.fields['trip_type'].label = "Trip Type"
       
       
       















       