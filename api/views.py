from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core import mail


from .serializers import ProductListSerializers, ProductDetailSerializers, CartSerializers

# models
from .models import Product, OrderProduct, Order
# Create your views here.

class ProductList(ListAPIView):

    # permission_classes = (AllowAny,)
    serializer_class = ProductListSerializers
    queryset = Product.objects.all()


class ProductDetail(APIView):

    def get(self, request):
        productName = request.GET.get('productName')
        item_detail = Product.objects.get(slug=productName)
        serializers = ProductDetailSerializers(item_detail)
        respone = Response(serializers.data, status=status.HTTP_200_OK)
        return respone


class addToCart(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        slug = request.data.get('slug', None)
        # print(slug)
        # print(request.user)
        if slug is None:
            return Response({'message': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        product_name = get_object_or_404(Product, slug = slug)
        order_item_qs, created = OrderProduct.objects.get_or_create(

            Product=product_name,
            user=request.user,
            ordered=False
        )

        order_qs = Order.objects.filter(user = request.user, ordered = False)

        if order_qs.exists():
            order = order_qs[0]

            if order.Product.filter(Product__slug=product_name.slug).exists():
                order_item_qs.quantity += 1
                order_item_qs.save()
                return Response(status=status.HTTP_200_OK)

            else:

                order.Product.add(order_item_qs)
                return Response(status=status.HTTP_200_OK)

        else:

            ordered_date = timezone.now()
            order = Order.objects.create(
                    user=request.user, 
                    ordered_date=ordered_date)
            order.Product.add(order_item_qs)
            return Response(status=status.HTTP_200_OK)



class removeFromCart(APIView):

    permission_classes = [IsAuthenticated]
    
    def post(self, request):

        print(request.user)
        slug = request.data.get('slug', None)
        if slug is None:
            return Response({'message': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        product_name = get_object_or_404(Product, slug = slug)
        order_qs = Order.objects.filter(user = request.user, ordered = False)
        if order_qs.exists():

            order = order_qs[0]

            if order.Product.filter(Product__slug=product_name.slug).exists():

                order_item = OrderProduct.objects.filter(

                    Product = product_name,
                    user = request.user,
                    ordered = False
                )[0]

                if order_item.quantity > 1:

                    order_item.quantity -= 1
                    order_item.save()
                    return Response({'messages':'This item was removed from your cart'},
                                    status=status.HTTP_200_OK)

                else:

                    order.Product.remove(order_item)
                    order_item.delete()
                    return Response({'messages':'This item was removed from your cart'},
                                    status=status.HTTP_200_OK)
            
            else:

                return Response({'messages':'This item was not in your cart'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:

            return Response({'messages':'You do not have an active order'},
                            status=status.HTTP_400_BAD_REQUEST)



class UserCart(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            order = Order.objects.get(user=request.user, ordered = False)
            serializers = CartSerializers(order)
            respone = Response(serializers.data, status=status.HTTP_200_OK)
            return respone 

        except ObjectDoesNotExist:
            return Response({'messages':'You do not have an active order'},
                            status=status.HTTP_400_BAD_REQUEST)


class Checkout(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        userOrder = Order.objects.get(user =request.user, ordered = False)
        subject = 'Thank You'
        message = render_to_string('email/order_checkout.html', {

            "username" : request.user.username,
            'name' : request.data.get('name'),
            'address' : request.data.get('address'),
            'Phone' : request.data.get('phone'),
            'Payment_option' : request.data.get('payment_option'),
            'object' : userOrder,

        })
        plain_message = ''
        from_email = 'noreply@cinnamone.com' 
        to = request.user.email
        # print('not notttttt')
        # print(to)
        # print(message)
        mail.send_mail(subject, plain_message, from_email, [to], html_message=message)
        return Response(status=status.HTTP_200_OK)