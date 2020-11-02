from django import forms
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Requisition
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.utils import timezone
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PassRequestMixin, PopRequestMixin, CreateUpdateAjaxMixin


class RequisitionModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:
        model = Requisition
        fields = ('requisition_no', 'item', 'quantity_requested', 'requesting_staff', 'department')


        widgets = {
        'requisition_no': forms.HiddenInput(),
        
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

       