from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
import json
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
from .models import *
from hr.models import *
from rrbnstaff.models import Request
from .mixins import RequisitionObjectMixin, RequisitionsObjectMixin, RequisitionCartItemObjectMixin, IssueObjectMixin
from .forms import *
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
from django.contrib.auth import get_user_model
User = get_user_model()
from formtools.wizard.views import SessionWizardView
from .utils import cookieCart, cartData, guestOrder

# Create your views here.

def is_valid_queryparam(param):
    return param != '' and param is not None

#@login_required
#def retrieve_item(request):
    #return render(request, 'store/retrieve_item.html')


# except:
    #     pass



        # stock_code = instance.stock_code
        # stock_code_int = int(stock_code[4:8])
        # instance.stock_code = str(instance.category.category_short) + str(stock_code_int).zfill(5)
        # instance.save()



# def increment_stock_code():
#     last_stock_code = Item.objects.all().order_by('stock_code').last()
#     if not last_stock_code:
#         return '00001'
        
#     new_stock_code = str(int(stock_code) + 1)
#     new_stock_code = stock_code[0:-(len(new_stock_code))] + new_stock_code
#     return new_stock_code

# def increment_stock_code():
#     last_stock_code = Item.objects.all().order_by('id').last()
#     if not last_stock_code:
#         return 'RNH' + '00001'
#     stock_code = last_stock_code.stock_code
#     stock_code_int = int(stock_code[4:8])
#     new_stock_code_int = stock_code_int + 1
#     new_stock_code = 'CAS' + str(new_stock_code_int).zfill(5)
#     return new_stock_code



# def increment_stock_code():
#     last_stock_code = Item.objects.all().order_by('id').last()
#     if not last_stock_code:
#         return 'RNH' + '00001'

#     if 'CAS' in last_stockode:
#         stock_code = last_stock_code.stock_code
#         stock_code_int = int(stock_code[4:8])
#         new_stock_code_int = stock_code_int + 1
#         new_stock_code = 'CAS' + str(new_stock_code_int).zfill(5)
#         return new_stock_code



 # def save(self, *args, **kwargs):
    #     super(Item, self).save(*args, **kwargs)
    #     p = Item.objects.get(id=self.id)
    #     # if p.category == "Computers & Accessories":
    #     stock_code = self.stock_code
    #     stock_code_int = int(stock_code[4:8])
    #     p.stock_code = str(self.category.category_name) + str(stock_code_int).zfill(5)
    #     p.save()


console.Log("Hello World")

var updateStockcode = document.getElementsByClassName('update-stock_code')

for (i = 0; i < updateStockcode.length; i++) {
    updateStockcode[i].addEventListener('click', function(){
        var itemId = this.dataset.item
        var action = this.dataset.action
        console.log('itemId:', itemId, 'Action:', action)
        console.log('USER:', user)
        updateStockCode(itemId, action)
        }
}


function updateStockCode(itemId, action){
    console.log('User is authenticated, sending data...')

        var url = '/store/create_stock_code/'

        fetch(url, {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
            }, 
            body:JSON.stringify({'itemId':itemId, 'action':action})
        })
        .then((response) => {
           return response.json();
        })
        // .then((data) => {
        //     location.reload()
        .then((data) => {
            console.Log('data:', data)
        });
}




# @receiver(post_save, sender=Item)
def update_stock_code_on_save(sender, instance, created, *args, **kwargs):
# def update_stock_code_on_save(sender, instance, **kwargs):
    post_save.disconnect(update_stock_code_on_save, sender=Item)
    item = instance
    # try:
    if instance.category.category_short == "CAS" and instance.id is not None:
        last_stock_code = Item.objects.filter(item_name=instance.item_name, category__category_short=instance.category.category_short).last()
        if not last_stock_code:
            return 'CAS' + '00001'
        stock_code = last_stock_code.stock_code
        new_stock_code = str(int(stock_code[4:8]) + 1)
        instance.stock_code = str(instance.category.category_short) + str(new_stock_code).zfill(5)
        
        instance.save()
        # post_save.connect(update_stock_code_on_save, sender=Item) 

    elif instance.category.category_short == "STA" and instance.id is not None:
        last_item = Item.objects.filter(category__category_short=instance.category.category_short).last()
        print(instance)
        print(last_item)
        if not last_item:
            instance.stock_code = 'STA' + '00001'
            print(instance.stock_code)
        stock_code = last_item.stock_code
        print(stock_code)
        stock_code_int = int(stock_code[4:8])
        new_stock_code_int = stock_code_int + 1
        # new_stock_code = str(int(stock_code[4:8]))
        instance.stock_code = str(instance.category.category_short) + str(new_stock_code_int).zfill(5)
        instance.save()
            # post_save.connect(update_stock_code_on_save, sender=Item) 
    



    elif instance.category.category_short == "CIT" and instance.id is not None:
        last_stock_code = Item.objects.filter(category__category_short=instance.category.category_short).last()
        if not last_stock_code:
            return 'CIT' + '00001'
        stock_code = last_stock_code.stock_code
        new_stock_code = str(int(stock_code[4:8]) + 1)
        instance.stock_code = str(instance.category.category_short) + str(new_stock_code).zfill(5)
        if created: 
            instance.save()
            post_save.connect(update_stock_code_on_save, sender=Item) 

    elif instance.category.category_short == "PMT" and instance.id is not None:
        last_stock_code = Item.objects.filter(category__category_short=instance.category.category_short).last()
        if not last_stock_code:
            return 'PMT' + '00001'
        # if not last_stock_code:
        #     return str(instance.category.category_short) + '00001'
        stock_code = last_stock_code.stock_code
        new_stock_code = str(int(stock_code[4:8]) + 1)
        instance.stock_code = str(instance.category.category_short) + str(new_stock_code).zfill(5)
        if created: 
            instance.save()
            post_save.connect(update_stock_code_on_save, sender=Item) 

    elif instance.category.category_short == "SUV" and instance.id is not None:
        last_stock_code = Item.objects.filter(category__category_short=instance.category.category_short).last()
        if not last_stock_code:
            return 'SUV' + '00001'
        # if not last_stock_code:
        #     return str(instance.category.category_short) + '00001'
        stock_code = last_stock_code.stock_code
        new_stock_code = str(int(stock_code[4:8]) + 1)
        instance.stock_code = str(instance.category.category_short) + str(new_stock_code).zfill(5)
        if created: 
            instance.save()
            post_save.connect(update_stock_code_on_save, sender=Item) 

    # else:
    #     # instance.category.id == 5
    #     last_stock_code = Item.objects.all().order_by('id').last()
    #     # if not last_stock_code:
    #     #     return str(instance.category.category_short) + '00001'
    #     stock_code = last_stock_code.stock_code
    #     new_stock_code = str(int(stock_code[4:8]) + 1)
    #     instance.stock_code = str(instance.category.category_short) + str(new_stock_code).zfill(5)
    #     instance.save()
    
post_save.connect(update_stock_code_on_save, sender=Item)   



# def update_stock_code_on_save(instance, **kwargs):
#     post_save.disconnect(update_stock_code_on_save, sender=Item)
#     # try:
#     if instance.category.category_short == "STA" and instance.id is not None:
#         last_stock_code = Item.objects.all().order_by('id').last()
#         stock_code = last_stock_code.stock_code
#         new_stock_code = str(int(stock_code[4:8]) + 1)
#         instance.stock_code = str(instance.category.category_short) + str(new_stock_code).zfill(5)
#         instance.save()
# post_save.connect(update_stock_code_on_save, sender=Item)




@login_required
def retrieve_item(request):
    data = cartData(request)
    requisitionCartItems = data['requisitionCartItems']
    requisitionCart = data['requisitionCart']
    qs = Item.objects.all()
    item_name = request.GET.get('item_name')

    if is_valid_queryparam(item_name):
        qs = qs.filter(item_name__iexact=item_name)


    context = {
        'queryset': qs, 'requisitionCartItems':requisitionCartItems,
    }
    return render(request, 'store/retrieve_item2.html', context)


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
        context['reqmnth'] = Requisition.objects.filter(requisition_creation_date__lt=this_month)
        context['issmnth'] = Issue.objects.filter(issue_date__lt=this_month)
        context['itemnth'] = Item.objects.filter(re_order_no__gt=F('quantity'), below_re_order_date__lt=this_month)
        context['resmnth'] = Item.objects.filter(Q(quantity__lte=0), below_re_order_date__lt=this_month)
       
        return context

@login_required
def store_dashboard(request):
    data = cartData(request)
    this_month = (datetime.datetime.now() + datetime.timedelta(days=30))

    requisitionCartItems = data['requisitionCartItems']
    requisitionCart = data['requisitionCart']
    items = data['items']
    products = Item.objects.all()
    requ =  Requisition.objects.all()
    iss =  IssueRequisition.objects.all()
    ite =  Item.objects.filter(re_order_no__gt=F('quantity'))
    res =  Item.objects.filter(Q(quantity__lte=0))
    reqmnth =  Requisition.objects.filter(requisition_creation_date__lt=this_month)
    issmnth =  IssueRequisition.objects.filter(issue_date__lt=this_month)
    itemnth =  Item.objects.filter(re_order_no__gt=F('quantity'), below_re_order_date__lt=this_month)
    resmnth =  Item.objects.filter(Q(quantity__lte=0), below_re_order_date__lt=this_month)
    context = {'products':products, 'requisitionCartItems':requisitionCartItems, 'requ':requ, 'iss':iss, 'ite':ite, 'res':res, 'reqmnth':reqmnth, 'issmnth':issmnth, 'itemnth':itemnth, 'resmnth':resmnth}
    return render(request, 'store/store_dashboard2.html', context)

def create_srv1(request, id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename = "SRV.pdf"'

    doc = SimpleDocTemplate(response,topMargin=20)
    doc.pagesize = landscape(A4)

    elements = []

    data= [

                 ['---OFFICE USE ONLY---'],
                 ['Date :','','ClassTeacher Signature: :',''],
                 ['Principal Signature :','','Accountant Signature :',''],
                 ['Student Name :'+' '+''],
                 ['Remark :','','',''],
          ]
    style =TableStyle([

                            ('SPAN',(2,15),(3,15)),
                            ('SPAN',(0,16),(1,16)),
                            ('SPAN',(2,16),(3,16)),
                            ('SPAN',(0,17),(3,17)),
                            ('SPAN',(0,18),(3,18)),
                    ])
    #Configure style and word wrap
    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'
    ps = ParagraphStyle('title', fontSize=15)
    data2 = [[Paragraph(cell, s) for cell in row] for row in data]
    t=Table(data2)
    t.setStyle(style)
    getSampleStyleSheet()
    elements.append(Paragraph("TRANSFER/DISCONTINUATION ACKNOWLEDGEMENT",ps))
    elements.append(Spacer(1,0.4*inch))
    elements.append(t)
    doc.build(elements)

    return response

def create_srv(request, id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename = "SRV.pdf"'
    
    doc = SimpleDocTemplate(response,topMargin=20)
    doc.pagesize = landscape(A5)
    elements = []
    styleSheet = getSampleStyleSheet()
    I = Image('static/img/logo_small.png')
    I.drawHeight = 1.25*inch*I.drawHeight / I.drawWidth
    I.drawWidth = 1.25*inch
    P0 = Paragraph('''
                   <b>A pa<font color=red>r</font>a<i>graph</i></b>
                   <super><font color=yellow>1</font></super>''',
                   styleSheet["BodyText"])
    P = Paragraph('''
        <para align=center spaceb=3>The <b>ReportLab Left
        <font color=red>Logo</font></b>
        Image</para>''',
        styleSheet["BodyText"])
    data= [['A', 'B', 'C', P0, 'D'],
           ['00', '01', '02', [I,P], '04'],
           ['10', '11', '12', [P,I], '14'],
           ['20', '21', '22', '23', '24'],
           ['30', '31', '32', '33', '34']]

    t=Table(data,style=[('GRID',(1,1),(-2,-2),1,colors.green),
                        ('BOX',(0,0),(1,-1),2,colors.red),
                        ('LINEABOVE',(1,2),(-2,2),1,colors.blue),
                        ('LINEBEFORE',(2,1),(2,-2),1,colors.pink),
                        ('BACKGROUND', (0, 0), (0, 1), colors.pink),
                        ('BACKGROUND', (1, 1), (1, 2), colors.lavender),
                        ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                        ('BOX',(0,0),(-1,-1),2,colors.black),
                        ('GRID',(0,0),(-1,-1),0.5,colors.black),
                        ('VALIGN',(3,0),(3,0),'BOTTOM'),
                        ('BACKGROUND',(3,0),(3,0),colors.limegreen),
                        ('BACKGROUND',(3,1),(3,1),colors.khaki),
                        ('ALIGN',(3,1),(3,1),'CENTER'),
                        ('BACKGROUND',(3,2),(3,2),colors.beige),
                        ('ALIGN',(3,2),(3,2),'LEFT'),
    ])
    t._argW[3]=1.5*inch
    elements.append(t)
    doc.build(elements)

    return response

def create_srv3(request, id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename = "SRV.pdf"'
    
    doc = SimpleDocTemplate(response,topMargin=20)
    doc.pagesize = landscape(A4)
    elements = []
    styleSheet = getSampleStyleSheet()

    I = Image('static/img/logo_small.png')
    I.drawHeight = 1.6*inch
    I.drawWidth = 2*inch
    data= [['','',I,'',''],
       ['Total Price', 'Price', 'QTY','Description', 'S.No'],
       ['00', 'rial 360,000', '02', '05', '04'],
       ['10', '11', '12', '06', '14'],
       ['20', '21', '22', '23', '24'],
       ['30', '31', '32', '33', '34']]
    t=Table(data)

    t.hAlign = 'CENTER'
    GRID_STYLE = TableStyle(
        [
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.white),

        ]
    )
    t.setStyle(GRID_STYLE)


    # colwidths = (60, 320, 60, 60)
    # t = Table(colwidths)
    # t.hAlign = 'RIGHT'
    # GRID_STYLE = TableStyle(
    #     [
    #         ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    #         ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    #         ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.white),

    #     ]
    # )
    # t.setStyle(GRID_STYLE)
    # return t



    elements.append(t) 
    doc.build(elements)





    return response

def create_srv1(request, id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename = "SRV.pdf"'

    doc = SimpleDocTemplate(response,topMargin=20)
    doc.pagesize = landscape(A4)

    elements = []

    data= [

                 ['---OFFICE USE ONLY---'],
                 ['Date :','','ClassTeacher Signature: :',''],
                 ['Principal Signature :','','Accountant Signature :',''],
                 ['Student Name :'+' '+''],
                 ['Remark :','','',''],
          ]
    style =TableStyle([

                            ('SPAN',(2,15),(3,15)),
                            ('SPAN',(0,16),(1,16)),
                            ('SPAN',(2,16),(3,16)),
                            ('SPAN',(0,17),(3,17)),
                            ('SPAN',(0,18),(3,18)),
                    ])
    #Configure style and word wrap
    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'
    ps = ParagraphStyle('title', fontSize=15)
    data2 = [[Paragraph(cell, s) for cell in row] for row in data]
    t=Table(data2)
    t.setStyle(style)
    getSampleStyleSheet()
    elements.append(Paragraph("TRANSFER/DISCONTINUATION ACKNOWLEDGEMENT",ps))
    elements.append(Spacer(1,0.4*inch))
    elements.append(t)
    doc.build(elements)

    return response

def create_srv4(request, id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'as_attachment=True; filename = "srv.pdf"'

    # doc = SimpleDocTemplate("form_letter.pdf",pagesize=A4,
    #                 rightMargin=72,leftMargin=72,
    #                 topMargin=72,bottomMargin=18)
    doc = SimpleDocTemplate(response,topMargin=20)
    doc.pagesize = portrait(A4)
    Story=[]
    logo = "static/img/logo_small.png"
    limitedDate = "03/05/2010"

    formatted_time = time.ctime()
    full_name = "Infosys"
    address_parts = ["411 State St.", "Marshalltown, IA 50158"]

    im = Image(logo, 1*inch, 1*inch,hAlign='LEFT')
    Story.append(im)

    Story.append(Spacer(1, 12))

    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='RIGHT', alignment=TA_RIGHT))


    ptext = '<font size=12>%s</font>' % formatted_time

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    # Create return address
    ptext = '<font size=12> Customer Name:  </font>'
    Story.append(Paragraph(ptext, styles["Normal"]))

    ptext = '<font size=12>%s</font>' % full_name
    Story.append(Paragraph(ptext, styles["Normal"]))       

    Story.append(Spacer(1,12))

    for part in address_parts:
      ptext = '<font size=12>%s</font>' % part.strip()
      Story.append(Paragraph(ptext, styles["RIGHT"]))   

    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Dear %s:</font>' % full_name.split()[0].strip()
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    ptext = '''<font size=12>We would like to welcome you to our subscriber base' 
    for  Magazine! \
        You will receive issues at the excellent introductory price of . Please 
        respond by\
         to start receiving your subscription and get the following: .</font>'''


    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    data = [[random.random() for i in range(1,4)] for j in range (1,8)]
    df = pd.DataFrame (data)

    lista = [df.columns[:,].values.astype(str).tolist()] + df.values.tolist()


    # restock = Restock.objects.all()

    # for obj in restock:
    #     Story.append(obj.restock_no)
    #     Story.append(obj.item_name)
    #     Story.append(obj.item_description)
    #     Story.append(obj.stock_code)
    #     Story.append(obj.unit)
    #     Story.append(obj.unit_price)
    #     Story.append(obj.quantity_ordered)
    #     Story.append(obj.quantity_received)




    t_style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                       ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                       ('VALIGN',(0,0),(0,-1),'TOP'),
                       ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                       ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ])
    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'
    t=Table(lista)
    t.setStyle(t_style)

    Story.append(t)
    Story.append(Spacer(1, 12))


    ptext = '<font size=12>Thank you very much and we look forward to serving you.</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Sincerely,</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 48))
    ptext = '<font size=12>Ima Sucker</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    doc.build(Story)
    
    return response
    # return FileResponse(as_attachment=True)


def create_srv2(request, id):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=landscape(A4))
    object = get_object_or_404(Restock, pk=id)



    image_path1 = '%s/img/cert_border5.jpeg' % settings.STATIC_ROOT
    image_path2 = '%s/img/logo_small.png' % settings.STATIC_ROOT
    image_path3 = '%s/img/cert_seal4.jpeg' % settings.STATIC_ROOT
    image_path4 = '%s/img/ceo_sign.jpg' % settings.STATIC_ROOT
    p.drawImage(image_path1, 0, 0, width=842, height=595)

    p.drawImage(image_path2, 380, 478, width=90, height=90)

  # Header Text
    p.setFont("Helvetica-Bold", 22, leading=None)
    p.drawCentredString(421, 450, 'THE RADIOGRAPHERS REGISTRATION BOARD OF NIGERIA')

  # Body Text
    p.setFont("Helvetica", 12, leading=None)
    p.drawCentredString(421, 435, 'Established by Decree 42, 1987 (now Cap R1 LFN 2004)')

    p.setFont("Helvetica", 9, leading=None)
    p.drawCentredString(670, 415, 'Stores Received Voucher No: '+ str(object.restock_no))

    p.setFont("Helvetica-Bold", 22, leading=None)
    p.drawCentredString(421, 390, 'Accreditation Certificate')

    p.setFont("Helvetica", 18, leading=None)
    p.drawCentredString(421, 360, 'This is to certify that')

    p.setFont("Helvetica", 22, leading=None)
    p.drawCentredString(421, 320, str(object.item_name))

    p.setFont("Helvetica", 14, leading=None)
    p.drawCentredString(421, 300, str(object.item_description))

    p.setFont("Helvetica", 16, leading=None)
    p.drawCentredString(421, 263, 'having satisfied all laid down conditions by Radiographers Registration Board of Nigeria')

    p.setFont("Helvetica", 16, leading=None)
    p.drawCentredString(421, 245, 'for accreditation of hospital/centre for training of Intern Radiographers')

    p.setFont("Helvetica", 16, leading=None)
    p.drawString(330, 200, 'have this day')

    p.setFont("Helvetica", 16, leading=None)
    p.drawString(435, 200, str(object.received_on))

    p.setFont("Helvetica", 16, leading=None)
    p.drawCentredString(300, 160, 'been granted')


    p.setFont("Helvetica", 16, leading=None)
    p.drawCentredString(455, 160, str(object.category))


    p.setFont("Helvetica", 16, leading=None)
    p.drawCentredString(300, 140, 'for the period')


    p.setFont("Helvetica", 16, leading=None)
    p.drawCentredString(400, 140, str(object.received_on))


    p.setFont("Helvetica", 16, leading=None)
    p.drawCentredString(455, 140, 'to')


    p.setFont("Helvetica", 16, leading=None)
    p.drawCentredString(511, 140, str(object.received_on))


    p.setFont("Helvetica", 14, leading=None)
    p.drawString(130, 100, 'Registrar/Secretary')

    p.drawImage(image_path3, 605, 65, width=120, height=120)
    p.drawImage(image_path4, 130, 110, width=110, height=60)

    p.setFont("Helvetica", 11, leading=None)
    p.drawCentredString(425, 45, 'This Certificate shall remain the propery of Radiographers Registration Board of Nigeria (RRBN) and shall, on demand, be surrendered to the Board')

    p.setFont("Helvetica", 11, leading=None)
    p.drawCentredString(425, 30, 'E-mail: info@rrbn.gov.ng')

    logo = ImageReader('static/img/logo.png')

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
   

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename='srv.pdf')


def add_item(request):
    data = cartData(request)

    requisitionCartItems = data['requisitionCartItems']
    requisitionCart = data['requisitionCart']
    items = data['items']

    products = Item.objects.all()
    context = {'products':products, 'requisitionCartItems':requisitionCartItems}
    return render(request, 'store/store.html', context)

@login_required
def find_item(request):
    data = cartData(request)
    requisitionCartItems = data['requisitionCartItems']
    requisitionCart = data['requisitionCart']
    items = data['items']
    # inventory = Item.objects.all()
    qs = Item.objects.all()
    query = request.GET.get('q')
    if query is not None:
        qs = qs.filter(item_name__icontains=query)
    else:
        qs = Item.objects.all()[:3]
    context = {
        'queryset': qs, 'requisitionCartItems':requisitionCartItems, 'items':items, 'requisitionCart':requisitionCart,
    }
    return render(request, 'store/add_to_cart.html', context)

@login_required
def cart(request):
    data = cartData(request)

    requisitionCartItems = data['requisitionCartItems']
    requisitionCart = data['requisitionCart']
    items = data['items']

    context = {'items':items, 'requisitionCart':requisitionCart, 'requisitionCartItems':requisitionCartItems}
    return render(request, 'store/requisition_cart.html', context)

def checkout(request):
    data = cartData(request)
    form = RequisitionsModelForm(request.POST, request.FILES)
    
    requisitionCartItems = data['requisitionCartItems']
    requisitionCart = data['requisitionCart']
    items = data['items']

    context = {'items':items, 'requisitionCart':requisitionCart, 'requisitionCartItems':requisitionCartItems, 'form':form}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    itemId = data['itemId']
    action = data['action']
    print('Action:', action)
    print('Item:', itemId)

    employee = request.user.employee
    item = Item.objects.get(id=itemId)
    requisition_cart, created = RequisitionCart.objects.get_or_create(employee=employee.employee, requisition_status=1)

    requisitionCartItem, created = RequisitionCartItem.objects.get_or_create(requisition_cart=requisition_cart, item=item)

    if action == 'add':
        requisitionCartItem.quantity = (requisitionCartItem.quantity + 1)
    elif action == 'remove':
        requisitionCartItem.quantity = (requisitionCartItem.quantity - 1)

    requisitionCartItem.save()

    if requisitionCartItem.quantity <= 0:
        requisitionCartItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    # transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        employee = request.user.employee
        requisition_cart, created = RequisitionCart.objects.get_or_create(employee=employee.employee, requisition_status=1)
        #requisition_cart, created = RequisitionCart.objects.get_or_create(requisition_status=1)
    # else:
    #     employee, requisition_cart = guestOrder(request, data)

    # total = float(data['form']['total'])
    # requisition_cart.transaction_id = transaction_id

    # if total == requisition_cart.get_cart_total:   
        requisition_cart.requisition_status = 2
        requisition_cart.save()

    # if requisition_cart.requisition_status == 2:

    # if requisition_cart.shipping == True:
    #if requisition_cart.requisition_status == 2:
        Requisition.objects.create(
        employee=Employee.objects.get(id=data['requisition']['employee']),
        requisition_cart=requisition_cart,
        requisition_reason=data['requisition']['requisition_reason'],
        hod=Employee.objects.get(id=data['requisition']['hod']),
    

        department=Department.objects.get(id=data['requisition']["department"]),

        #department=data['requisition']['department'],
      
        )

    return JsonResponse('Payment submitted..', safe=False)


class IssueInternalRequisition(RequisitionObjectMixin, SuccessMessageMixin, CreateView):
    template_name = 'store/issue_requisition2.html'
    form_class = IssueRequisitionsModelForm
    formset_class =IssueRequisitionItemFormSet
    success_message = 'Requisition issued successfully'
    success_url = reverse_lazy('store:issue_list') 

    def get_context_data(self, *args, **kwargs):
        context = super(IssueInternalRequisition, self).get_context_data(**kwargs)
        obj = get_object_or_404(RequisitionCart,  requisition_no=self.get_requisition())
        qs = RequisitionCart.objects.filter(requisition=self.get_requisition())
        qs1 = obj.requisitioncartitem_set.all()
        #formset =IssueRequisitionItemFormSet(queryset=qs, initial=[{'requisition':self.get_requisition()}]) 
        formset =IssueRequisitionItemFormSet(queryset=qs1) 
        form = IssueRequisitionsModelForm(initial={'requisition':self.get_requisition()})

        data = cartData(self.request)
        requisitionCartItems = data['requisitionCartItems']

        context['requisitionCartItems'] = requisitionCartItems
        context['requisition_formset'] = formset
        context['form'] = form  
        context['object'] = self.get_requisition()
        return context   

    def post(self, request, *args, **kwargs):
        self.object = self.get_requisition()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        obj = get_object_or_404(RequisitionCart,  requisition_no=self.get_requisition())
        qs1 = obj.requisitioncartitem_set.all()
        formsets = IssueRequisitionItemFormSet(self.request.POST, queryset=qs1)

        if form.is_valid() and formsets.is_valid():
            formsets.save()   
            form.save()
        return super().post(request, *args, **kwargs)

class RequisitionListView(LoginRequiredMixin, ListView):
    template_name = "store/requisitions_list2.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Requisition.objects.order_by('-requisition_creation_date')
        

    def get_context_data(self, **kwargs):
        obj = super(RequisitionListView, self).get_context_data(**kwargs)
        obj['requisition_qs'] = Requisition.objects.filter(requisition_status=1)
        data = cartData(self.request)
        requisitionCartItems = data['requisitionCartItems']

        obj['requisitionCartItems'] = requisitionCartItems
        return obj

# class RequisitionDetailsView(LoginRequiredMixin, RequisitionObjectMixin, View):
#     template_name = "store/requisition_detail2.html" 
#     def get(self, request, id=None, *args, **kwargs):
#         context = {'object': self.get_requisition()}
#         return render(request, self.template_name, context) 


class RequisitionDetailsView(LoginRequiredMixin, DetailView):
    template_name = "store/requisition_detail2.html"
    model = Requisition

    def get_context_data(self, *args, **kwargs):
        context = super(RequisitionDetailsView, self).get_context_data(**kwargs)
        data = cartData(self.request)
        requisitionCartItems = data['requisitionCartItems']

        context['requisitionCartItems'] = requisitionCartItems
        return context   



class IssuedRequisitions(LoginRequiredMixin, ListView):
    template_name = "store/issued_requisitions.html"
    context_object_name = 'object'

    def get_queryset(self):
        return IssueRequisition.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(IssuedRequisitions, self).get_context_data(**kwargs)
        obj['issued_requisitions_qs'] = IssueRequisition.objects.all()
        return obj

class IssuedRequisitionsDetailView(LoginRequiredMixin, DetailView):
    template_name = "store/issued_requisitions_details2.html"
    model = IssueRequisition


class RequisitionUpdateView(UpdateView):
    model = Requisition
    form_class = RequisitionsUpdateModelForm
    formset_class = RequisitionItemFormSet
    template_name = 'store/requisition_update3.html'
    success_url = reverse_lazy('store:requisition_list')

    def get_context_data(self, *args, **kwargs):
        context = super(RequisitionUpdateView, self).get_context_data(**kwargs)
        qs = RequisitionCart.objects.filter(requisition=self.get_object())
        obj = get_object_or_404(RequisitionCart,  requisition_no=self.get_object())
        qs1 = obj.requisitioncartitem_set.all()
        formset =RequisitionItemFormSet(queryset=qs1) 
        data = cartData(self.request)
        requisitionCartItems = data['requisitionCartItems']
        context['requisitionCartItems'] = requisitionCartItems
        # formset = RequisitionItemFormSet(queryset=qs, initial=[{'requisition':self.get_object()}])
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
        qs = RequisitionCart.objects.filter(requisition=self.get_object())
        # qs = RequisitionItem.objects.filter(requisition=self.get_object())
        obj = get_object_or_404(RequisitionCart,  requisition_no=self.get_object())
        qs1 = obj.requisitioncartitem_set.all()
        # formsets = RequisitionItemFormSet(self.request.POST, queryset=qs, initial=[{'requisition':self.get_object()}])
        formsets = RequisitionItemFormSet(self.request.POST, queryset=qs1)

        if form.is_valid() and formsets.is_valid():
            form.save()
            formsets.save()
        return super().post(request, *args, **kwargs)
            # new_instances = formsets.save(commit=False)
            # for new_instance in new_instances:
            #     new_instance.requisition = self.get_object()
            #     new_instance.save()
        #     return self.form_valid(form)
        # else:
        #     return self.form_invalid(form)

class IssueRequisitionUpdate(LoginRequiredMixin, IssueObjectMixin, UpdateView):
    model = IssueRequisition
    template_name = 'store/issue_requisition_update2.html'
    form_class = IssueRequisitionsModelForm
    formset_class = IssueRequisitionItemFormSet
    success_message = 'Issued Requisition updated successfully'
    success_url = reverse_lazy('store:issue_list')

    def get_context_data(self, *args, **kwargs):
        context = super(IssueRequisitionUpdate, self).get_context_data(**kwargs)
        # qs = RequisitionCart.objects.filter(requisition=self.get_object())
        obj = get_object_or_404(RequisitionCart,  requisition_no=self.get_object())
        qs1 = obj.requisitioncartitem_set.all()
        formset =IssueRequisitionItemFormSet(queryset=qs1) 

        # qs = RequisitionCartItem.objects.filter(requisition_cart__issuerequisition=self.get_object())
        # formset = IssueRequisitionItemFormSet(queryset=qs)
        context['requisition_formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # qs = RequisitionCartItem.objects.filter(requisition_cart__issuerequisition=self.get_object())
        obj = get_object_or_404(RequisitionCart,  requisition_no=self.get_object())
        qs1 = obj.requisitioncartitem_set.all()




        formsets = IssueRequisitionItemFormSet(self.request.POST, queryset=qs1)

        if form.is_valid() and formsets.is_valid():
            form.save()
            formsets.save()    
        
        return super().post(request, *args, **kwargs)


# class IssueRequisitionUpdate(LoginRequiredMixin, IssueObjectMixin, UpdateView):
#     model = IssueRequisition
#     template_name = 'store/issue_requisition_update2.html'
#     form_class = IssueRequisitionsModelForm
#     formset_class = IssueRequisitionItemFormSet
#     success_message = 'Issued Requisition updated successfully'
#     success_url = reverse_lazy('store:issue_list')

#     def get_context_data(self, *args, **kwargs):
#         context = super(IssueRequisitionUpdate, self).get_context_data(**kwargs)
#         qs = RequisitionItem.objects.filter(requisition__issue=self.get_object())
#         formset = IssueRequisitionItemFormSet(queryset=qs)
#         context['requisition_formset'] = formset
#         return context

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         qs = RequisitionItem.objects.filter(requisition__issue=self.get_object())
#         formsets = IssueRequisitionItemFormSet(self.request.POST, queryset=qs)

#         if form.is_valid() and formsets.is_valid():
#             form.save()
#             formsets.save()    
        
#         return super().post(request, *args, **kwargs)

class RequisitionWizard(SessionWizardView):
    form_list = [RequisitionsModelForm, RequisitionItemFormSet]
    template_name = 'store/formwizard.html'
    # def done(self, form_list, **kwargs):
    #     do_something_with_the_form_data(form_list)
    #     return HttpResponseRedirect("/")
        # return HttpResponseRedirect(reverse("store:find_item"))

    def done(self, form_list, **kwargs):
        form_data = [form.cleaned_data for form in form_list]
        # requisition_data = Requisition(requisition_reason = form_data[0]['requisition_reason'], requesting_staff = form_data[0]['requesting_staff'], authorized_by = form_data[0]['authorized_by'], department = form_data[0]['department'],)
        # requisition_data.save( )
        # requisitionitem_data = RequisitionItem(requisition = form_data[0]['requisition'], item = form_data[0]['item'], quantity = form_data[0]['quantity'])
        form.save( )
        return render(self.request, 'store/emptylist.html', {'data': form_data})


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

class ItemCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'store/create_item2.html'
    form_class = ItemModelForm
    success_message = 'Item created Successfully.'

    success_url = reverse_lazy('store:items_list')

def load_users(request):
    department_id = request.GET.get('department')
    users = User.objects.filter(department_id=department_id)
    return render(request, 'store/user_dropdown_list_options.html', {'users': users})



class CreateRequisitionItems(View):
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

class CreateRequisitionItems(View):
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
            requisition.department = request.user.department
            requisition.requesting_staff = request.user
            requisition.authorized_by = request.user
            requisition.save()
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete")
        if item_id:
            item_instance = get_object_or_404(Item, id=item_id)
            qty = request.GET.get("qty")
            requisition_item = RequisitionItem.objects.get_or_create(requisition=requisition, item=item_instance)[0]
            if delete_item:
                requisition_item.delete()
            else:
                requisition_item.quantity = qty
                requisition_item.save()
        return HttpResponseRedirect("/")



# class RequestItem(LoginRequiredMixin, CreateView):
#     model = Requisition
#     form_class = RequisitionsModelForm
#     formset_class = RequisitionItemFormSet
#     template_name = 'store/requisition_update3.html'
#     success_url = reverse_lazy('store:requisition_list')

#     def get_context_data(self, *args, **kwargs):
#         context = super(RequestItem, self).get_context_data(**kwargs)
#         # qs = RequisitionItem.objects.filter(requisition=self.get_object())
#         # qs = RequisitionItem.objects.all()
#         formset = RequisitionItemFormSet()
#         context['requisition_formset'] = formset
#         return context

#     # def get_initial(self):
#     #     return {
#     #         'requisition': self.kwargs["pk"],   
#     #     }

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         # qs = RequisitionItem.objects.all()
#         formsets = RequisitionItemFormSet(self.request.POST)

#         if form.is_valid() and formsets.is_valid():
#             form.save()

#             new_instances = formsets.save(commit=False)
#             for new_instance in new_instances:
#                 new_instance.requisition = self.get_object()
#                 new_instance.save()

#             formsets.save()    
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)


class RequestItem(LoginRequiredMixin, CreateView):
    model = Requisition
    template_name = 'store/requisition_create_list.html'
    form_class = RequisitionsModelForm
    success_url = reverse_lazy('store:requisition_list')

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(0)
        requisition_id = self.request.session.get("requisition_id")
        if requisition_id == None:
            requisition = Requisition()
            requisition.save()
            requisition_id = requisition.id
            requisition.department = self.request.user.department
            requisition.requesting_staff = self.request.user
            requisition.authorized_by = self.request.user
            requisition.save()
            self.request.session["requisition_id"] = requisition_id
        requisition, created = Requisition.objects.get_or_create(id=requisition_id)
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
                return HttpResponseRedirect(reverse("store:find_item"))
       

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
        # return self.form_invalid(form)


# class RequestItem(LoginRequiredMixin, CreateView):
#     model = Requisition
#     template_name = 'store/requisition_create_list.html'
#     form_class = RequisitionsModelForm

#     def get(self, request, *args, **kwargs):
#         request.session.set_expiry(0)
#         requisition_id = request.session.get("requisition_id")
#         if requisition_id == None:
#             requisition = Requisition()
#             # if request.user.is_authenticated():
#             requisition.department = request.user.department
#             requisition.requesting_staff = request.user
#             requisition.authorized_by = request.user
#             requisition.save()
                
#             requisition_id = requisition.id
#             request.session["requisition_id"] = requisition_id
#         requisition = Requisition.objects.get(id=requisition_id)
#         return requisition

        
#         item_id = request.GET.get("item")
#         delete_item = request.GET.get("delete")
#         if item_id:
#             item_instance = get_object_or_404(Item, id=item_id)
#             qty = request.GET.get("qty", 1)
#             try:
#                 if int(qty) < 1:
#                     delete_item = True
#             except:
#                 raise Http404
#             requisition_item, created = RequisitionItem.objects.get_or_create(requisition=requisition, item=item_instance)
            
#             if created:
#                 flash_message = "Item added to requisition list"
#                 item_added = True
#             if delete_item:
#                 flash_message = "Item removed from requisition list"
#                 requisition_item.delete()
#             else:
#                 if not created:
#                     flash_message = "Requisition list item successfully updated"
#                 requisition_item.quantity = qty
#                 requisition_item.save()
#             if not request.is_ajax():
#                 return HttpResponseRedirect(reverse("store:find_item"))
       

#         if request.is_ajax():
#             try:
#                 total = requisition_item.line_item_total
#             except:
#                 total = None
#             data = {
#                     "deleted": delete_item,
#                     "item_added": item_added,
#                     "line_total": total,
#                     "flash_message": flash_message,

#                     }
#             return JsonResponse(data)

#         context = {
            
#             "form":self.get_form(),
#             "object":requisition
#         }
#         template = self.template_name
#         return render(request, template, context)

  

#     def post(self, request, *args, **kwargs):
#         # requisition = Requisition.objects.get(id=requisition_id)
#         self.object = requisition
#         form = self.get_form()
#         if form.is_valid():
#             requisition = form.save(commit=False)
#             del request.session["requisition_id"]
#             requisition.save()

#         return self.form_valid(form)
#         return self.form_invalid(form)        


    







# class RequisitionDetailsView(LoginRequiredMixin, DetailView):
#     template_name = "store/requisition_detail2.html" 
#     model = Requisition

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


# class IssueRequisition(RequisitionObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):









class ItemObjectMixin(object):
    model = Item
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj





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

