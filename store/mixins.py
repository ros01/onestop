from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rrbnstaff.models import RequisitionItem, Requisition
from django.shortcuts import get_object_or_404, render, redirect

from django.http import Http404


class StaffRequiredMixin(object):
	@classmethod
	def as_view(self, *args, **kwargs):
		view = super(StaffRequiredMixin, self).as_view(*args, **kwargs)
		return login_required(view)

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_staff:
			return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)
		else:
			raise Http404



class LoginRequiredMixin(object):
	@classmethod
	def as_view(self, *args, **kwargs):
		view = super(LoginRequiredMixin, self).as_view(*args, **kwargs)
		return login_required(view)

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)



class RequisitionObjectMixin(object):
    model = Requisition
    def get_requisition(self):
        id = self.kwargs.get('id')
        requisition = None
        if id is not None:
            requisition = get_object_or_404(self.model, id=id)
        return requisition 


class RequisitionItemObjectMixin(object):
    model = RequisitionItem
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 