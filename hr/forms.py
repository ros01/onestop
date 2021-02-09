from django import forms
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Employee, Driver, Performance, Leave, Location, Title, Grade, Specify, Document, Category, Vendor, Training, Record, Appraisal, Schedule, Discipline, Compliance, Course
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


class TrainingModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    
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
        model = Training
        fields = ('training_name', 'training_description', 'category', 'vendor', 'staff_name', 'projected_start_date', 'projected_end_date', 'training_venue', 'training_budget', 'added_by')

        widgets = {
            'training_description': forms.Textarea(attrs={'readonly': True,'rows':3, 'cols':5}), 
            'training_name': forms.TextInput(attrs={'readonly': True}), 
                    
            }

    def __init__(self, *args, **kwargs):
       super(TrainingModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       self.fields['training_name'].label = "Training Name"
       self.fields['training_name'].widget.attrs['placeholder'] = "Enter Training Name"
       self.fields['training_description'].label = "Training Description"
       self.fields['training_description'].widget.attrs['placeholder'] = "Enter Training Description"
       self.fields['category'].label_from_instance = lambda obj: "{}".format(obj.category_name)
       self.fields['category'].widget.attrs['readonly'] = 'readonly'
       self.fields['category'].label = "Training Category"
       self.fields['vendor'].label_from_instance = lambda obj: "{}".format(obj.vendor_name)
       self.fields['vendor'].widget.attrs['readonly'] = 'readonly'
       self.fields['vendor'].label = "Vendor"
       self.fields['staff_name'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)
       self.fields['staff_name'].label = "Staff Name"
       self.fields['staff_name'].widget = CheckboxSelectMultiple()
       self.fields['staff_name'].queryset = User.objects.all()
       self.fields['projected_start_date'].label = "Training Projected Start Date"
       self.fields['projected_start_date'].widget.attrs['placeholder'] = "Enter Training Projected Start Date"
       self.fields['projected_end_date'].label = "Training Projected End Date"
       self.fields['projected_end_date'].widget.attrs['placeholder'] = "Enter Training Projected End Date"
       self.fields['training_venue'].label = "Training Venue"
       self.fields['training_venue'].widget.attrs['placeholder'] = "Enter Training Venue"
       self.fields['training_budget'].label = "Training Budget"
       self.fields['training_budget'].widget.attrs['placeholder'] = "Enter Training Budget"
     
    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance


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



class AssignLeaveRequestModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    approved_start_date = forms.DateField(
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

    approved_end_date = forms.DateField(
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
        model = Specify
        fields = ('request_no', 'staff_name', 'requested_start_date', 'requested_end_date', 'approved_start_date', 'approved_end_date', 'comments', 'leave_type', 'leave_application_date', 'assigned_by')
        widgets = {
        #'leave_application_date': forms.HiddenInput(),
        'leave_application_date': forms.TextInput(attrs={'readonly': True}),
        'request_no': forms.TextInput(attrs={'readonly': True}), 
        'comments': forms.Textarea(attrs={'rows':2, 'cols':3}),
        'leave_type': forms.TextInput(attrs={'readonly': True}), 
        'requested_start_date': forms.TextInput(attrs={'readonly': True}),
        'requested_end_date': forms.TextInput(attrs={'readonly': True}),        
        }

    def __init__(self, *args, **kwargs):
       super(AssignLeaveRequestModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       self.fields['request_no'].label = "Request No"
       self.fields['staff_name'].widget.attrs['readonly'] = 'readonly'
       self.fields['staff_name'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)
       self.fields['staff_name'].label = "Staff Name"
       self.fields['requested_start_date'].label = "Requested Start Date"
       self.fields['requested_end_date'].label = "Requested End Date"
       self.fields['leave_application_date'].label = "Leave Application Date"
       self.fields['leave_type'].label = "Leave Type"
       self.fields['approved_start_date'].label = "Approved Start Date"
       self.fields['approved_end_date'].label = "Approved End Date"
       self.fields['comments'].label = "Comments"
       

    def save(self):
      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)
      return instance
       
class EndLeaveModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    actual_start_date = forms.DateField(
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

    actual_end_date = forms.DateField(
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
        model = Document
        fields = ('request_no', 'staff_name', 'leave_type', 'leave_application_date', 'requested_start_date', 'requested_end_date', 'approved_start_date', 'approved_end_date', 'actual_start_date', 'actual_end_date', 'comments',  'documented_by')
        widgets = {
        #'leave_application_date': forms.HiddenInput(),
        'leave_application_date': forms.TextInput(attrs={'readonly': True}),
        'request_no': forms.TextInput(attrs={'readonly': True}), 
        'comments': forms.Textarea(attrs={'rows':2, 'cols':3}),
        'leave_type': forms.TextInput(attrs={'readonly': True}), 
        'requested_start_date': forms.TextInput(attrs={'readonly': True}),
        'requested_end_date': forms.TextInput(attrs={'readonly': True}), 
        'approved_start_date': forms.TextInput(attrs={'readonly': True}),
        'approved_end_date': forms.TextInput(attrs={'readonly': True}),        
        }

    def __init__(self, *args, **kwargs):
       super(EndLeaveModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       self.fields['request_no'].label = "Request No"
       self.fields['staff_name'].widget.attrs['readonly'] = 'readonly'
       self.fields['staff_name'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)
       self.fields['staff_name'].label = "Staff Name"
       self.fields['requested_start_date'].label = "Requested Start Date"
       self.fields['requested_end_date'].label = "Requested End Date"
       self.fields['approved_start_date'].label = "Approved Start Date"
       self.fields['approved_end_date'].label = "Approved End Date"
       self.fields['leave_application_date'].label = "Leave Application Date"
       self.fields['leave_type'].label = "Leave Type"
       self.fields['actual_start_date'].label = "Actual Start Date"
       self.fields['actual_end_date'].label = "Actual End Date"
       self.fields['comments'].label = "Comments"
       

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
        fields = ('vendor_name', 'description', 'address', 'phone', 'email' ,'added_by')

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


class CourseModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    
    class Meta:
        model = Course
        fields = ('training_name', 'training_description', 'category', 'vendor', 'added_by')

        widgets = {
            'training_description': forms.Textarea(attrs={'rows':2, 'cols':3}),   
            }

    def __init__(self, *args, **kwargs):
       super(CourseModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       self.fields['training_name'].label = "Training Name"
       self.fields['training_name'].widget.attrs['placeholder'] = "Enter Training Name"
       self.fields['training_description'].label = "Training Description"
       self.fields['training_description'].widget.attrs['placeholder'] = "Enter Training Description"
       self.fields['category'].label = "Training Category"
       self.fields['category'].widget.attrs['placeholder'] = "Enter Training Category"
       self.fields['vendor'].label = "Training Vendor"
       self.fields['vendor'].widget.attrs['placeholder'] = "Enter Training Vendor"
       
     
    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance







class RecordModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    training_start_date = forms.DateField(
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

    training_end_date = forms.DateField(
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
        model = Record
        fields = ('training_name', 'training_description', 'category', 'vendor', 'staff_name', 'projected_start_date', 'projected_end_date', 'training_venue', 'training_budget', 'training_start_date', 'training_end_date', 'training_cost')

        widgets = {
            'training_description': forms.Textarea(attrs={'rows':2, 'cols':3}),   
            }
       
    def __init__(self, *args, **kwargs):
       super(RecordModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
       self.fields['training_name'].label = "Training Name"
       self.fields['training_name'].widget.attrs['placeholder'] = "Enter Training Name"
       self.fields['training_description'].label = "Training Description"
       self.fields['training_description'].widget.attrs['placeholder'] = "Enter Training Description"
       self.fields['category'].label = "Training Category"
       self.fields['category'].widget.attrs['placeholder'] = "Enter Training Category"
       self.fields['vendor'].label = "Training Vendor"
       self.fields['vendor'].widget.attrs['placeholder'] = "Enter Training Vendor"
       self.fields['staff_name'].label = "Staff Name"
       self.fields['staff_name'].widget.attrs['placeholder'] = "Enter Staff Name"
       self.fields['projected_start_date'].label = "Training Projected Start Date"
       self.fields['projected_start_date'].widget.attrs['placeholder'] = "Enter Training Projected Start Date"
       self.fields['projected_end_date'].label = "Training Projected End Date"
       self.fields['projected_end_date'].widget.attrs['placeholder'] = "Enter Training Projected End Date"
       self.fields['staff_name'].widget.attrs['placeholder'] = "Enter Staff Name"
       self.fields['training_start_date'].label = "Training Start Date"
       self.fields['training_start_date'].widget.attrs['placeholder'] = "Enter Training Start Date"
       self.fields['training_end_date'].label = "Training End Date"
       self.fields['training_end_date'].widget.attrs['placeholder'] = "Enter Training End Date"
       self.fields['training_venue'].label = "Training Venue"
       self.fields['training_venue'].widget.attrs['placeholder'] = "Enter Training Venue"
       self.fields['training_budget'].label = "Training Budget"
       self.fields['training_budget'].widget.attrs['placeholder'] = "Enter Training Budget"
       self.fields['training_cost'].label = "Training Cost"
       self.fields['training_cost'].widget.attrs['placeholder'] = "Enter Training Cost"
       

    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance


class AppraisalModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
        
    class Meta:
        model = Appraisal
        fields = ('appraisal_name', 'description', 'added_by')

        widgets = {
            'description': forms.Textarea(attrs={'rows':2, 'cols':3}),   
            }

                

    def __init__(self, *args, **kwargs):
       super(AppraisalModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
      
       self.fields['appraisal_name'].label = "Appraisal Name"
       self.fields['appraisal_name'].widget.attrs['placeholder'] = "Enter Appraisal Name"
       self.fields['description'].label = "Description"
       self.fields['description'].widget.attrs['placeholder'] = "Enter Description"
             
    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance


class ScheduleModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    appraisal_due_date = forms.DateField(
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
        model = Schedule
        fields = ('schedule_no', 'staff_name', 'appraisal', 'appraisal_due_date', 'projected_start_date', 'projected_end_date', 'appraisal_scheduled_by')
        

    def __init__(self, *args, **kwargs):
       super(ScheduleModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       
       self.fields['staff_name'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)
       self.fields['staff_name'].label = "Staff Name"
       self.fields['appraisal'].label = "Appraisal Type"
       self.fields['appraisal'].widget.attrs['placeholder'] = "Enter Appraisal Type"
       self.fields['appraisal_due_date'].label = "Appraisal Due Date"
       self.fields['appraisal_due_date'].widget.attrs['placeholder'] = "Enter Appraisal Due Date"
       self.fields['projected_start_date'].label = "Projected Start Date"
       self.fields['projected_start_date'].widget.attrs['placeholder'] = "Enter Projected Start Date"
       self.fields['projected_end_date'].label = "Projected End Date"
       self.fields['projected_end_date'].widget.attrs['placeholder'] = "Enter Projected End Date"
              

    def save(self):
      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)
      return instance


class PerformanceEvaluationModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    appraisal_start_date = forms.DateField(
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

    appraisal_end_date = forms.DateField(
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
        model = Performance
        fields = ('schedule_no', 'staff_name', 'appraisal', 'appraisal_due_date', 'projected_start_date', 'projected_end_date', 'appraisal_start_date', 'appraisal_end_date', 'comments', 'score', 'appraised_by')
        widgets = {
        
        'schedule_no': forms.TextInput(attrs={'readonly': True}), 
        'comments': forms.Textarea(attrs={'rows':2, 'cols':3}),
        #'appraisal': forms.TextInput(attrs={'readonly': True}),
        'appraisal_due_date': forms.TextInput(attrs={'readonly': True}), 
        'projected_start_date': forms.TextInput(attrs={'readonly': True}),
        'projected_end_date': forms.TextInput(attrs={'readonly': True}),         
        }

    def __init__(self, *args, **kwargs):
       super(PerformanceEvaluationModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       self.fields['schedule_no'].label = "Schedule No"
       self.fields['staff_name'].widget.attrs['readonly'] = 'readonly'
       self.fields['staff_name'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)
       self.fields['staff_name'].label = "Staff Name"
       self.fields['appraisal'].label_from_instance = lambda obj: "{}".format(obj.appraisal_name)
       self.fields['appraisal'].widget.attrs['readonly'] = 'readonly'
       self.fields['appraisal'].label = "Appraisal Type"
       self.fields['appraisal_due_date'].label = "Appraisal Due Date"
       self.fields['projected_start_date'].label = "Scheduled Start Date"
       self.fields['projected_end_date'].label = "Scheduled End Date"
       self.fields['appraisal_start_date'].label = "Appraisal Start Date"
       self.fields['appraisal_start_date'].widget.attrs['placeholder'] = "Select Appraisal Start Date"
       self.fields['appraisal_end_date'].label = "Appraisal End Date"
       self.fields['appraisal_end_date'].widget.attrs['placeholder'] = "Select Appraisal End Date"
       self.fields['score'].label = "Appraisal Score"
       self.fields['score'].widget.attrs['placeholder'] = "Enter Appraisal Score"
       self.fields['comments'].label = "Appraisal Comments"
       self.fields['comments'].widget.attrs['placeholder'] = "Enter Appraisal Comments"
       
    def save(self):
      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)
      return instance



class DisciplineModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    due_date = forms.DateField(
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
        model = Discipline
        fields = ('case_no', 'staff_name', 'case_name', 'case_description', 'penalty', 'due_date', 'assigned_by')
        widgets = {     
        'case_description': forms.Textarea(attrs={'rows':2, 'cols':3}),        
        }

    def __init__(self, *args, **kwargs):
       super(DisciplineModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       
       self.fields['staff_name'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)
       self.fields['staff_name'].label = "Staff Name"
       self.fields['case_name'].label = "Case Name"
       self.fields['case_name'].widget.attrs['placeholder'] = "Enter Case Name"
       self.fields['case_description'].label = "Case Description"
       self.fields['case_description'].widget.attrs['placeholder'] = "Enter Case Description"
       self.fields['penalty'].label = "Penalty"
       self.fields['penalty'].widget.attrs['placeholder'] = "Enter Penalty"
       self.fields['due_date'].label = "Due Date"
       self.fields['due_date'].widget.attrs['placeholder'] = "Enter Due Date"
              

    def save(self):
      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)
      return instance


class ComplianceModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    completed_on = forms.DateField(
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
        model = Compliance
        fields = ('case_no', 'staff_name', 'case_name', 'case_description', 'penalty', 'due_date', 'case_status', 'completed_on', 'closed_by')
        widgets = {
        
        'case_no': forms.TextInput(attrs={'readonly': True}), 
        'case_name': forms.TextInput(attrs={'readonly': True}),
        #'case_description': forms.Textarea(attrs={'rows':2, 'cols':3}),
        'case_description': forms.Textarea(attrs={'readonly': True,'rows':2, 'cols':12}),
        'penalty': forms.TextInput(attrs={'readonly': True}), 
        'due_date': forms.TextInput(attrs={'readonly': True}),
               
        }

    def __init__(self, *args, **kwargs):
       super(ComplianceModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       
       self.fields['staff_name'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)
       self.fields['staff_name'].label = "Staff Name"
       self.fields['staff_name'].widget.attrs['readonly'] = 'readonly'
       self.fields['case_name'].label = "Case Name"
       self.fields['case_name'].widget.attrs['placeholder'] = "Enter Case Name"
       self.fields['case_description'].label = "Case Description"
       self.fields['case_description'].widget.attrs['placeholder'] = "Enter Case Description"
       self.fields['penalty'].label = "Penalty"
       self.fields['penalty'].widget.attrs['placeholder'] = "Enter Penalty"
       self.fields['due_date'].label = "Due Date"
       self.fields['due_date'].widget.attrs['placeholder'] = "Enter Due Date"
       self.fields['case_status'].label = "Case Status"
       self.fields['case_status'].widget.attrs['placeholder'] = "Update Case Status"
       self.fields['completed_on'].label = "Completed On"
       self.fields['completed_on'].widget.attrs['placeholder'] = "Enter Completed On"
       
    def save(self):
      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)
      return instance