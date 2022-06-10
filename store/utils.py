import json
from .models import *

def cookieCart(request):

	#Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		print('CART:', cart)

	items = []
	requisitionCart = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
	requisitionCartItems = requisitionCart['get_cart_items']

	for i in cart:
		#We use try block to prevent items in cart that may have been removed from causing error
		try:	
			if(cart[i]['quantity']>0): #items with negative quantity = lot of freebies  
				requisitionCartItems += cart[i]['quantity']

				item = Item.objects.get(id=i)
				total = (item.price * cart[i]['quantity'])

				requisitionCart['get_cart_total'] += total
				requisitionCart['get_cart_items'] += cart[i]['quantity']

				item = {
				'id':item.id,
				'item':{'id':item.id,'name':item.item_name,  
				'imageURL':item.imageURL}, 'quantity':cart[i]['quantity'],
				'get_total':total,
				}
				items.append(item)

				# if product.digital == False:
				# 	requisition['shipping'] = True
		except:
			pass
			
	return {'requisitionCartItems':requisitionCartItems ,'requisitionCart':requisitionCart, 'items':items}

def cartData(request):
	if request.user.is_authenticated:
		employee = request.user
		requisitionCart, created = RequisitionCart.objects.get_or_create(employee=employee, requisition_status=1)
		items = requisitionCart.requisitioncartitem_set.all()
		requisitionCartItems = requisitionCart.get_requisition_cart_items
	else:
		cookieData = cookieCart(request)
		requisitionCartItems = cookieData['requisitionCartItems']
		requisitionCart = cookieData['requisitionCart']
		items = cookieData['items']

	return {'requisitionCartItems':requisitionCartItems ,'requisitionCart':requisitionCart, 'items':items}


def restockcartData(request):
	if request.user.is_authenticated:
		staff_name = request.user
		restockCart, created = RestockCart.objects.get_or_create(staff_name=staff_name, complete=False)
		items = restockCart.restockcartitem_set.all()
		restockCartItems = restockCart.get_restock_cart_items
	else:
		items = []
		restockCart = {'get_restock_cart_items':0, 'get_restock_cart_total':0}
		restockCartItems = restockCart['get_restock_cart_items']

	return {'restockCartItems':restockCartItems ,'restockCart':restockCart, 'items':items}

	



	
def guestOrder(request, data):
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	employee, created = Employee.objects.get_or_create(
			email=email,
			)
	employee.name = name
	employee.save()

	requisitionCart = Requisition.objects.create(
		employee=employee,
		# complete=False,
		)

	for item in items:
		product = Item.objects.get(id=item['id'])
		requisitionCartItem = RequisitionCartItem.objects.create(
			product=product,
			requisitionCart=requisitionCart,
			quantity=(item['quantity'] if item['quantity']>0 else -1*item['quantity']), # negative quantity = freebies
		)
	return employee, requisitionCart