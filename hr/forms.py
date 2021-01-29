from django import forms
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Employee, Driver, Department, Performance, Leave, Learning, Location, Title, Grade
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.utils import timezone
from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_modal_forms.mixins import PassRequestMixin, PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from tempus_dominus.widgets import DatePicker, DateTimePicker


class JobTitleModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:
        model = Title
        fields = ('job_title', 'description',)

        widgets = {
            'description': forms.Textarea(attrs={'rows':2, 'cols':3}),   
            }

                

    def __init__(self, *args, **kwargs):
       super(JobTitleModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
       self.fields['job_title'].label = "Job Title"
       self.fields['job_title'].widget.attrs['placeholder'] = "Enter Job Title"
       self.fields['description'].label = "Description"
       self.fields['description'].widget.attrs['placeholder'] = "Enter Description"
       

    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance



class PayGradeModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:
        model = Grade
        fields = ('pay_grade_name', 'paygrade_description', 'pay_grade_code', 'added_by')
        
        widgets = {
            'paygrade_description': forms.Textarea(attrs={'rows':2, 'cols':3}),   
            }            

    def __init__(self, *args, **kwargs):
       super(PayGradeModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       self.fields['pay_grade_name'].label = "Pay Grade"
       self.fields['pay_grade_name'].widget.attrs['placeholder'] = "Enter Pay Grade"
       self.fields['paygrade_description'].label = "Pay Grade Description"
       self.fields['paygrade_description'].widget.attrs['placeholder'] = "Enter Pay Grade Description"
       self.fields['pay_grade_code'].label = "Pay Grade Code"
       self.fields['pay_grade_code'].widget.attrs['placeholder'] = "Enter Pay Grade Code"
       
    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance



