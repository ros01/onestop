from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
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


class CartOrderMixin(object):
	def get_order(self, *args, **kwargs):
		cart = self.get_cart()
		if cart is None:
			return None
		new_order_id = self.request.session.get("order_id")
		if new_order_id is None:
			new_order = Order.objects.create(cart=cart)
			self.request.session["order_id"] = new_order.id
		else:
			new_order = Order.objects.get(id=new_order_id)
		return new_order

	def get_cart(self, *args, **kwargs):
		cart_id = self.request.session.get("cart_id")
		if cart_id == None:
			return None
		cart = Cart.objects.get(id=cart_id)
		if cart.items.count() <= 0:
			return None
		return cart

class IssueObjectMixin(object):
    model = IssueRequisition
    def get_issue(self):
        id = self.kwargs.get('id')
        issue = None
        if id is not None:
            issue = get_object_or_404(self.model, id=id)
        return issue 


class RequisitionObjectMixin(object):
    model = Requisition
    def get_requisition(self):
        id = self.kwargs.get('id')
        requisition = None
        if id is not None:
            requisition = get_object_or_404(self.model, id=id)
        return requisition 

    
class RequisitionCartObjectMixin(object):
    model = RequisitionCart
    def get_requisition_cart(self):
        id = self.kwargs.get('id')
        requisition_cart = None
        if id is not None:
            requisition_cart = get_object_or_404(self.model, id=id)
        return requisition_cart 

class RequisitionsObjectMixin(object):
    model = Requisition
    def get_requisition(self):
        pk = self.kwargs.get('pk')
        requisition = None
        if pk is not None:
            requisition = get_object_or_404(self.model, pk=pk)
        return requisition 


class RequisitionCartItemObjectMixin(object):
    model = RequisitionCartItem
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 