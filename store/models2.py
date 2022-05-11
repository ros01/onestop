from django.db import models


class Item(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_name = models.CharField(max_length=200)
    item_description = models.TextField()
    #requisition = models.ForeignKey(Requisition, related_name='items_requisition',  on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, related_name='default_category', null=True,  on_delete=models.DO_NOTHING)
    stock_code = models.CharField(max_length=200, unique=True)
    vendor = models.ForeignKey(Vendor, null=True, on_delete=models.DO_NOTHING)
    unit = models.CharField(max_length=100, choices = UNIT_OF_MEASUREMENT)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=20)
    re_order_no = models.IntegerField()
    item_image = models.ImageField(upload_to='%Y/%m/%d/', blank=True)
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    entry_date = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)
    below_re_order_date = models.DateField(default=date.today, blank=True)
    unavailable_date = models.DateField(default=date.today, blank=True)
    
    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return self.item.get_absolute_url()

    def get_absolute_url(self):
        return reverse("store:item_detail", kwargs={"pk": self.pk})

    def add_to_requisition(self):
        return "%s?item=%s&qty=1" %(reverse("store:create_item_requisition"), self.id)

    def remove_from_requisition(self):
        return "%s?item=%s&qty=1&delete=True" %(reverse("store:create_item_requisition"), self.id)

    def get_success_url(self):
        return reverse("store:item_detail", kwargs={"id": self.object.id})

    class Meta:
        ordering = ["-entry_date"]


    @property
    def imageURL(self):
        try:
            url = self.item_image.url
        except:
            url = ''
        return url


class RequisitionCart(models.Model):
	employee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requisition_created_by', blank=True, on_delete=models.DO_NOTHING)
    requisition_date = models.DateField(auto_now_add=True, auto_now=False)
    requisition_status = models.IntegerField(default=1)
    requisition_no = models.CharField(max_length=500, null=True, blank=True, 
        default=increment_requisition_no)

    def __str__(self):
        return str(self.requisition_no)

    # def get_absolute_url(self):
    #     return reverse("store:requisition_details", kwargs={"id": self.id})
        
    @property
    def get_requisition_cart_total(self):
        requisitionitems = self.requisitionitem_set.all()
        total = sum([item.get_total for item in requisitionitems])
        return total 

    @property
    def get_requisition_cart_items(self):
        requisitionitems = self.requisitionitem_set.all()
        total = sum([item.quantity for item in requisitionitems])
        return total 

    # class Meta:
    #     unique_together = ('requisition_no','employee')
    #     ordering = ["-requisition_date"]
    
class RequisitionCartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    requisition_cart = models.ForeignKey(RequisitionCart, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    # quantity_issued = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    # def __str__(self):
    #     return self.item.item_name
    
    def __str__(self):
        return str(self.requisition_cart.requisition_no)


    def remove(self):
        return self.item.remove_from_requisition()   

class Requisition(models.Model):
	employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	requisition_cart = models.ForeignKey(RequisitionCart, on_delete=models.SET_NULL, null=True)
    requisition_reason = models.TextField(blank=True)
    authorized_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_by', blank=True, on_delete=models.DO_NOTHING)
    department = models.ForeignKey('hr.Department', related_name='requesting_department', blank=True, on_delete=models.CASCADE)
    requisition_creation_date = models.DateField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return str(self.requisition_cart.requisition_no)

class Issue(models.Model):
	employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	requisition_cart = models.ForeignKey(RequisitionCart, on_delete=models.SET_NULL, null=True)
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE)
    # requisition_items = models.ForeignKey(RequisitionItem, on_delete=models.CASCADE)
    # requisition_items = models.ManyToManyField(RequisitionItem)
    quantity_issued = models.IntegerField(default=0, null=True, blank=True)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='issuing_staff',  on_delete=models.DO_NOTHING)
    issue_date = models.DateField(default=date.today, blank=True)
    
    # def __str__(self):
    #     return str(self.requisition)    

    def __str__(self):
        return str(self.requisition_cart.requisition_no)
    
    
