from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import (
     CreateView,
     DetailView,
     ListView,
     UpdateView,
     DeleteView,
     TemplateView
)
from .models import Category, Item, Vendor, Issue, Restock
from rrbnstaff.models import RequisitionItem, Requisition, Request
from .mixins import RequisitionObjectMixin, RequisitionItemObjectMixin
from .forms import ItemModelForm, CategoryModelForm, VendorModelForm, IssueRequisitionModelForm, RestockModelForm, RequisitionModelForm, RequisitionForm, RequisitionsModelForm, RequisitionItemModelForm, RequisitionItemFormSet, RequisitionItemForm, RequisitionForm
from django.forms import modelformset_factory
#from rrbnstaff.forms import RequisitionModelForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from bootstrap_modal_forms.generic import BSModalCreateView
from bootstrap_modal_forms.mixins import PassRequestMixin, CreateUpdateAjaxMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q, Count, F, Value
from django.core.exceptions import ObjectDoesNotExist
import datetime

# Create your views here.

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "store/store_dashboard2.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(DashboardTemplateView, self).get_context_data(*args, **kwargs)
        this_month = (datetime.datetime.now() + datetime.timedelta(days=30))
        context['requ'] = Requisition.objects.all()
        context['iss'] = Issue.objects.all()
        context['ite'] = Item.objects.filter(re_order_no__gt=F('quantity'))
        context['res'] = Item.objects.filter(Q(quantity__lte=0))
        context['reqmnth'] = Requisition.objects.filter(requisition_date__lt=this_month)
        context['issmnth'] = Issue.objects.filter(issue_date__lt=this_month)
        context['itemnth'] = Item.objects.filter(re_order_no__gt=F('quantity'), below_re_order_date__lt=this_month)
        context['resmnth'] = Item.objects.filter(Q(quantity__lte=0), below_re_order_date__lt=this_month)
        return context


class ItemCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'store/create_item2.html'
    form_class = ItemModelForm
    success_message = 'Item created Successfully.'

    success_url = reverse_lazy('store:items_list')

class RequisitionListView(LoginRequiredMixin, ListView):
    template_name = "store/requisitions_list2.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Requisition.objects.order_by('-requisition_date')
        

    def get_context_data(self, **kwargs):
        obj = super(RequisitionListView, self).get_context_data(**kwargs)
        obj['requisition_qs'] = Requisition.objects.filter(requisition_status=1)
        return obj

class RequisitionDetailsView(LoginRequiredMixin, RequisitionObjectMixin, View):
    template_name = "store/requisition_detail2.html" 
    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_requisition()}
        return render(request, self.template_name, context) 


class RequisitionDeleteView(LoginRequiredMixin, RequisitionObjectMixin, View):
    template_name = "store/requisition_delete.html" # DetailView
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_requisition()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_requisition()
        if obj is not None:
            obj.delete()
            context['object'] = None
            return redirect('store:requisition_list')
        return render(request, self.template_name, context)

class RequisitionUpdateView2(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Requisition
    template_name = 'store/requisition_update.html'
    form_class = RequisitionForm
    success_message = 'Success: Requisition Items updated.'
    success_url = reverse_lazy('store:requisition_list')


    def get_form(self, *args, **kwargs):
        form = super(RequisitionUpdateView, self).get_form(*args, **kwargs)

        print (form)
        
        return form

def is_valid_queryparam(param):
    return param != '' and param is not None

@login_required
def retrieve_item(request):
    qs = Item.objects.all()
    item_name = request.GET.get('item_name')

    if is_valid_queryparam(item_name):
        qs = qs.filter(item_name__iexact=item_name)


    context = {
        'queryset': qs,
    }
    return render(request, 'store/retrieve_item2.html', context)



@login_required
def find_item(request):
    qs = Item.objects.all()
    query = request.GET.get('q')
    qs = qs.filter(item_name__icontains=query)
    context = {
        'queryset': qs,
    }
    return render(request, 'store/item_results.html', context)

class RequestItem(LoginRequiredMixin, UpdateView):
    model = Requisition
    template_name = 'store/requisition_create_list.html'
    form_class = RequisitionsModelForm

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(0)
        requisition_id = self.request.session.get("requisition_id")
        if requisition_id == None:
            requisition = Requisition()
            requisition.save()
            requisition_id = requisition.id
            self.request.session["requisition_id"] = requisition_id
        requisition = Requisition.objects.get(id=requisition_id)
        #if self.request.user.is_authenticated():
            #requisition.user = request.user
        requisition.save()
        return requisition


    def get(self, request, *args, **kwargs):
        requisition = self.get_object()
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete", False)
        flash_message = ""
        item_added = False
        if item_id:
            item_instance = get_object_or_404(Item, id=item_id)
            qty = request.GET.get("qty", 1)
            try:
                if int(qty) < 1:
                    delete_item = True
            except:
                raise Http404
            requisition_item, created = RequisitionItem.objects.get_or_create(requisition=requisition, item=item_instance)
            
            if created:
                flash_message = "Item added to requisition list"
                item_added = True
            if delete_item:
                flash_message = "Item removed from requisition list"
                requisition_item.delete()
            else:
                if not created:
                    flash_message = "Requisition list item successfully updated"
                requisition_item.quantity = qty
                requisition_item.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse("store:create_item_requisition"))
       

        if request.is_ajax():
            try:
                total = requisition_item.line_item_total
            except:
                total = None
            data = {
                    "deleted": delete_item,
                    "item_added": item_added,
                    "line_total": total,
                    "flash_message": flash_message,

                    }
            return JsonResponse(data)

        context = {
            
            "form":self.get_form(),
            "object":self.get_object()
        }
        template = self.template_name
        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            requisition = form.save(commit=False)
            del request.session["requisition_id"]
            requisition.save()

        return self.form_valid(form)
        return self.form_invalid(form)
        



class RequisitionUpdateView(LoginRequiredMixin, UpdateView):
    model = Requisition
    form_class = RequisitionsModelForm
    formset_class = RequisitionItemFormSet
    template_name = 'store/requisition_update3.html'
    success_url = reverse_lazy('store:requisition_list')

    def get_context_data(self, *args, **kwargs):
        context = super(RequisitionUpdateView, self).get_context_data(**kwargs)
        qs = RequisitionItem.objects.filter(requisition=self.get_object())
        formset = RequisitionItemFormSet(queryset=qs, initial=[{'requisition':self.get_object()}])
        context['requisition_formset'] = formset
        return context

    def get_initial(self):
        return {
            'requisition': self.kwargs["pk"],   
        }

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        qs = RequisitionItem.objects.filter(requisition=self.get_object())
        formsets = RequisitionItemFormSet(self.request.POST, queryset=qs)

        if form.is_valid() and formsets.is_valid():
            form.save()

            new_instances = formsets.save(commit=False)
            for new_instance in new_instances:
                new_instance.requisition = self.get_object()
                new_instance.save()

            formsets.save()    
            return self.form_valid(form)
        return self.form_invalid(form)


# class RequisitionUpdateView(UpdateView):
#     #model = Requisition
#     template_name = 'store/requisition_update2.html'
#     form_class = RequisitionsModelForm
#     success_message = 'Success: Requisition Items updated.'
#     success_url = reverse_lazy('store:requisition_list')


#     def get_object(self):
#         id_ = self.kwargs.get("id")
#         return get_object_or_404(Requisition, id = id_)

#     def form_valid(self, form):
#         print(form.cleaned_data)
#         return super().form_valid(form)


# class IssueRequisitionUpdate(LoginRequiredMixin, IssueObjectMixin, View):
#     template_name = "store/issue_requisition_update.html" 
#     template_name1 = "store/issue_requisition_details2.html" 
    
#     def get(self, request, id=None, *args, **kwargs):
#         # GET method
#         context = {}
#         obj = self.get_object()
#         if obj is not None:
#             form = IssueRequisitionModelForm(instance=obj)
#             context['object'] = obj
#             context['form'] = form
#         return render(request, self.template_name, context)

#     def post(self, request, id=None,  *args, **kwargs):
#         # POST method
#         context = {}
#         obj = self.get_object()
#         if obj is not None:
#             form = IssueRequisitionModelForm(request.POST or None, instance=obj)
#             if form.is_valid():
#                 form.save()
#             context['object'] = obj
#             context['form'] = form
#             context['issue'] = Issue.objects.filter (requisition_no=obj.requisition_no)
#         messages.success(request, ('Requisition Update Successful'))
#         return render(request, self.template_name1, context)








#@login_required
#def retrieve_item(request):
    #return render(request, 'store/retrieve_item.html')





class ItemObjectMixin(object):
    model = Item
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj


class ItemCountView(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            requisition_id = self.request.session.get("requisition_id")
            if requisition_id == None:
                count = 0
            else:
                requisition = Requisition.objects.get(id=requisition_id)
                count = requisition.items.count()
            request.session["requisition_item_count"] = count
            return JsonResponse({"count": count})
        else:
            raise Http404







class RequisitionCheckout(LoginRequiredMixin, DetailView):
    model = Requisition
    template_name = "store/requisition_checkout.html"
    #form_class = GuestCheckoutForm

    def get_object(self, *args, **kwargs):
        requisition_id = self.request.session.get("requisition_id")
        if requisition_id == None:
            return redirect("store:create_item_requisition")
        requisition = Requisition.objects.get(id=requisition_id)
        return requisition

    def get_context_data(self, *args, **kwargs):
        context = super(RequisitionCheckout, self).get_context_data(*args, **kwargs)
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            
    def get_success_url(self):
        return reverse("store:requisition_list")
 





    
#class RequisitionUpdateView(View):
    #model = Requisition
    #form_class = RequisitionModelForm

    #template_name = 'store/requisition_update.html'

    #def get(self, request, *args, **kwargs):
        #item_id = request.GET.get("item")
        #if item_id:
            #item_instance = get_object_or_404(Item, id=item_id)
            #qty = request.GET.get("qty")
            #requisition = Requisition.objects.all().first()
            #requisition_item = RequisitionItem.objects.get_or_create(requisition=requisition, item=item_instance)[0]
            #requisition_item.quantity = 200
            #requisition_item.save()
            #print (requisition_item)

        #context = {
            
        #}
        #template = self.template_name
        #return render(request, template, context)



    




class RequisitionCheckout1(DetailView):
    model = Requisition
    template_name = "store/requisition_checkout.html"
    #form_class = GuestCheckoutForm

    def get_object(self, *args, **kwargs):
        cart = self.get_cart()
        if cart == None:
            return None
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)
        user_can_continue = False
        user_check_id = self.request.session.get("user_checkout_id")
        if self.request.user.is_authenticated():
            user_can_continue = True
            user_checkout, created = UserCheckout.objects.get_or_create(email=self.request.user.email)
            user_checkout.user = self.request.user
            user_checkout.save()
            context["client_token"] = user_checkout.get_client_token()
            self.request.session["user_checkout_id"] = user_checkout.id
        elif not self.request.user.is_authenticated() and user_check_id == None:
            context["login_form"] = AuthenticationForm()
            context["next_url"] = self.request.build_absolute_uri()
        else:
            pass

        if user_check_id != None:
            user_can_continue = True
            if not self.request.user.is_authenticated(): #GUEST USER
                user_checkout_2 = UserCheckout.objects.get(id=user_check_id)
                context["client_token"] = user_checkout_2.get_client_token()
        
        #if self.get_cart() is not None:
        context["order"] = self.get_order()
        context["user_can_continue"] = user_can_continue
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user_checkout, created = UserCheckout.objects.get_or_create(email=email)
            request.session["user_checkout_id"] = user_checkout.id
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("checkout")


    def get(self, request, *args, **kwargs):
        get_data = super(CheckoutView, self).get(request, *args, **kwargs)
        cart = self.get_object()
        if cart == None:
            return redirect("cart")
        new_order = self.get_order()
        user_checkout_id = request.session.get("user_checkout_id")
        if user_checkout_id != None:
            user_checkout = UserCheckout.objects.get(id=user_checkout_id)
            if new_order.billing_address == None or new_order.shipping_address == None:
                return redirect("order_address")
            new_order.user = user_checkout
            new_order.save()
        return get_data


class RequestItem1(View):
    def get(self, request, *args, **kwargs):
        requisition_id = request.GET.get("item")
        delete_item = request.GET.get("delete")
        if requisition_id:
            item_instance = get_object_or_404(Item, id=item_id)
            qty = request.GET.get("qty")
            requisition = Requisition.objects.all().first()
            requisition_item = RequisitionItem.objects.get_or_create(requisition=requisition, item=item_instance)[0]
            if delete_item:
                requisition_item.delete()
            else:
                requisition_item.quantity = qty
                requisition_item.save()
        return HttpResponseRedirect("/")


class RequestItemOld(View):
    def get(self, request, *args, **kwargs):
        request.session.set_expiry(0)
        requisition_id = request.session.get("requisition_id")
        if requisition_id == None:
            requisition = Requisition()
            requisition.save()
            requisition_id = requisition.id
            request.session["requisition_id"] = requisition_id
        requisition = Requisition.objects.get(id=requisition_id)
        if request.user.is_authenticated():
            requisition.user = request.user
            requisition.save()
        requisition_id = request.GET.get("item")
        delete_item = request.GET.get("delete")
        if requisition_id:
            item_instance = get_object_or_404(Item, id=item_id)
            qty = request.GET.get("qty")
            requisition_item = RequisitionItem.objects.get_or_create(requisition=requisition, item=item_instance)[0]
            if delete_item:
                requisition_item.delete()
            else:
                requisition_item.quantity = qty
                requisition_item.save()
        return HttpResponseRedirect("/")




class CreateRequisition(LoginRequiredMixin, ItemObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'store/create_requisition.html'
    form_class = RequisitionModelForm
    success_message = 'Requisition created successfully'
    success_url = reverse_lazy('rrbnstaff:requisition_list') 

    def get_context_data(self, *args, **kwargs):
        context = super(CreateRequisition, self).get_context_data(**kwargs)
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = RequisitionModelForm(instance=obj)
            context['object'] = obj  
            context['form'] = form
        return context   

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data())

@login_required
def restock(request):
    try:
        query = request.GET.get('q')
        object = 0

    except ValueError:
        query = None
        object = None
    try:
        object = Item.objects.get(
            Q(stock_code=query) | Q(item_name__icontains=query)
        )

    except ObjectDoesNotExist:
        messages.error(request, ('Stock Code or Item Name is Invalid.  Enter a Valid Stock Code or Item Name'))
        pass

    return render(request, 'store/results.html', {"object": object})


class ItemObjectMixin(object):
    model = Item
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class RestockItem(LoginRequiredMixin, ItemObjectMixin, View):
    template_name = "store/restock_item.html"
    template_name1 = "store/restock_item_details.html"
    
    def get(self, request,  *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = RestockModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form

        return render(request, self.template_name, context)



    def post(self, request,  *args, **kwargs):
        
        form = RestockModelForm(request.POST)
        if form.is_valid():
            if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
                form.save(commit=False)
            else:
                form.save(commit=True)
            
        context = {}

        obj = self.get_object()
        if obj is not None:
            form = RestockModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
            context['restock'] = Restock.objects.filter (stock_code=obj.stock_code, restock_no= request.POST['restock_no'])

        return render(request, self.template_name1, context)


class ReceivedItemsList(LoginRequiredMixin, ListView):
    template_name = "store/restock_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Restock.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(ReceivedItemsList, self).get_context_data(**kwargs)
        obj['restock_qs'] = Restock.objects.order_by('-received_on')
        return obj


class ItemRestockDetails(LoginRequiredMixin, DetailView):
    template_name = "store/restock_details.html"
    model = Restock


class VendorListView(LoginRequiredMixin, ListView):
    template_name = "store/vendors_list2.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Vendor.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(VendorListView, self).get_context_data(**kwargs)
        obj['vendor_qs'] = Vendor.objects.order_by('-date_created')
        return obj

class ItemCategoyListView(LoginRequiredMixin, ListView):
    template_name = "store/items_category_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Category.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(ItemCategoyListView, self).get_context_data(**kwargs)
        obj['category_qs'] = Category.objects.order_by('-entry_date')
        return obj

class ItemsListView(LoginRequiredMixin, ListView):
    template_name = "store/items_list2.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Item.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(ItemsListView, self).get_context_data(**kwargs)
        obj['items_qs'] = Item.objects.order_by('-entry_date')
        return obj





class IssuedRequisitions(LoginRequiredMixin, ListView):
    template_name = "store/issued_requisitions.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Issue.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(IssuedRequisitions, self).get_context_data(**kwargs)
        obj['issued_requisitions_qs'] = Issue.objects.all()
        return obj


class VendorCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'store/create_vendor2.html'
    form_class = VendorModelForm
    success_message = 'Vendor created Successfully.'

    success_url = reverse_lazy('store:vendor_list')

class CategoryCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'store/create_category2.html'
    form_class = CategoryModelForm
    success_message = 'Category created Successfully.'

    success_url = reverse_lazy('store:category_list')



class VendorObjectMixin(object):
    model = Vendor
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 

class CategoryObjectMixin(object):
    model = Category
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


   

class IssueObjectMixin(object):
    model = Issue
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 



class IssueRequisition(LoginRequiredMixin, RequisitionObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'store/issue_requisition.html'
    form_class = IssueRequisitionModelForm
    success_message = 'Requisition issued successfully'
    success_url = reverse_lazy('store:issue_list') 

    def get_context_data(self, *args, **kwargs):
        context = super(IssueRequisition, self).get_context_data(**kwargs)
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = IssueRequisitionModelForm(instance=obj)
            context['object'] = obj  
            context['form'] = form
        return context   
   
    def form_invalid(self, form):
        form = self.get_form()
        context = {}
        obj = self.get_object()
        if obj is not None:  
           context['object'] = obj
           context['form'] = form 
        return self.render_to_response(context)

#class IssueRequisition(LoginRequiredMixin, RequisitionObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    #template_name = 'store/issue_requisition.html'
    #template_name1 = 'store/issue_requisition_details2.html'
    #def get(self, request,  *args, **kwargs):
        #context = {}
        #obj = self.get_object()
        #if obj is not None:
            #form = IssueRequisitionModelForm(instance=obj)
            #context['object'] = obj
            #context['form'] = form

        #return render(request, self.template_name, context)


    #def post(self, request,  *args, **kwargs):
        #form = IssueRequisitionModelForm(request.POST)
        #if form.is_valid():
            #if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
                #form.save(commit=False)
            #else:
                #form.save(commit=True)  
        #context = {}
        #obj = self.get_object()
        #if obj is not None:
            #form = IssueRequisitionModelForm(instance=obj)
            #context['object'] = obj
            #context['form'] = form
            #context['issue'] = Issue.objects.filter (requisition_no=obj.requisition_no)
        #return render(request, self.template_name1, context)


class ItemDetailView(LoginRequiredMixin, DetailView):
    template_name = "store/item_detail2.html"
    model = Item




class ItemListView(ListView):
    template_name = "store/item_list_detail.html"
    model = Item
    queryset = Item.objects.all()


    def get_queryset(self, *args, **kwargs):
        qs = super(ItemListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        print (self.kwargs)
        return qs


class IssuedRequisitionsDetailView(LoginRequiredMixin, DetailView):
    template_name = "store/issued_requisitions_details.html"
    model = Issue



class VendorDetailView(LoginRequiredMixin, VendorObjectMixin, View):
    template_name = "store/vendor_detail2.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)


class VendorUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Vendor
    template_name = 'store/vendor_update2.html'
    form_class = VendorModelForm
    success_message = 'Success: Vendor Details were updated.'
    success_url = reverse_lazy('store:vendor_list')



class VendorDeleteView(LoginRequiredMixin, VendorObjectMixin, View):
    template_name = "store/vendor_delete2.html" # DetailView
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            obj.delete()
            context['object'] = None
            return redirect('store:vendor_list')
        return render(request, self.template_name, context)


class ItemUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Item
    template_name = 'store/item_update2.html'
    form_class = ItemModelForm
    success_message = 'Success: Item details were updated.'
    success_url = reverse_lazy('store:items_list')



class ItemDeleteView(LoginRequiredMixin, ItemObjectMixin, View):
    template_name = "store/item_delete2.html" # DetailView
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            obj.delete()
            context['object'] = None
            return redirect('store:items_list')
        return render(request, self.template_name, context)


class CategoryDetailView(LoginRequiredMixin, CategoryObjectMixin, View):
    template_name = "store/category_detail2.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)


class CategoryUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Category
    template_name = 'store/category_update2.html'
    form_class = CategoryModelForm
    success_message = 'Success: Category details were updated.'
    success_url = reverse_lazy('store:category_list')


class CategoryDeleteView(LoginRequiredMixin, CategoryObjectMixin, View):
    template_name = "store/category_delete2.html" # DetailView
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            obj.delete()
            context['object'] = None
            return redirect('store:category_list')
        return render(request, self.template_name, context)





class IssueRequisitionDetail(LoginRequiredMixin, IssueObjectMixin, View):
    template_name = "store/issue_requisition_details2.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)

 
class IssueRequisitionUpdate(LoginRequiredMixin, IssueObjectMixin, View):
    template_name = "store/issue_requisition_update.html" 
    template_name1 = "store/issue_requisition_details2.html" 
    
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = IssueRequisitionModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = IssueRequisitionModelForm(request.POST or None, instance=obj)
            if form.is_valid():
                form.save()
            context['object'] = obj
            context['form'] = form
            context['issue'] = Issue.objects.filter (requisition_no=obj.requisition_no)
        messages.success(request, ('Requisition Update Successful'))
        return render(request, self.template_name1, context)
