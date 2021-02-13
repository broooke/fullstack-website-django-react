from django.shortcuts import render

from base.products import products
from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import ProductSerializer, OrderSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
	user = request.user
	data = request.data

	orderItems = data['orderItems']

	if orderItems and len(orderItems) == 0:
		return Response({'detail':'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
	else:
		order = Order.objects.create(
			user=user,
			paymentMethod=data['paymentMethod'],
			taxPrice=data['taxPrice'],
			shippingPrice=data['shippingPrice'],
			totalPrice=data['totalPrice'],
			)

		shipping = ShippingAddress.objects.create(
			order=order,
			phone=data['shippingAddress']['phone'],
			address=data['shippingAddress']['address'],
			city=data['shippingAddress']['city'],
			postalCode=data['shippingAddress']['postalCode'],
			country=data['shippingAddress']['country'],
			)

		for item in orderItems:
			product = Product.objects.get(_id=item['product'])
			itemOrder = OrderItem.objects.create(
				order=order,
				product=product,
				name=product.name,
				qty=item['qty'],
				price=item['price'],
				image=product.image.url,
				)

			product.countInStock-=itemOrder.qty
			product.save()

		serializer = OrderSerializer(order, many=False)
		return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):

	user = request.user

	try:
		order = Order.objects.get(_id=pk)
		if user.is_staff or order.user == user:
			serializer = OrderSerializer(order,many=False)
			return Response(serializer.data)
		else:
			return Response({'detail':'Not authorized to view this order'}, status=HTTP_400_BAD_REQUEST)
	except:
		return Response({'detail':'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
	order = Order.objects.get(_id=pk)

	order.isPaid = True
	order.paidAt = datetime.now()
	order.save()

	return Response('Order was paid')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
	user = request.user
	orders = Order.objects.filter(user=user)
	serializer = OrderSerializer(orders, many=True)
	return Response(serializer.data)


