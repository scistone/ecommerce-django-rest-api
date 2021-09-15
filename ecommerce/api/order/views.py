import iyzipay
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render,redirect

from rest_framework import status
from rest_framework.generics import CreateAPIView,GenericAPIView,ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import SessionAuthentication

from order.models import Order, OrderItem
from .serializers import OrderSerializer
from knox.auth import TokenAuthentication



class CreateOrderView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

    def get_client_ip(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self,request,*args,**kwargs):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            iyzico_options = settings.IYZICO_OPTIONS
            paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])
            
            basketItems = []
            for item in serializer.validated_data['items']:
                basketItem = dict([('id', item.get('product').id)])
                basketItem['name'] = item.get('product').title
                basketItem['category1'] = 'None'
                basketItem['itemType'] = 'PHYSICAL'
                basketItem['price'] = float(item.get('quantity')*item.get('product').price)
                basketItems.append(basketItem)




            callback_url = settings.URL + '/api/order/payment-callback/'

            buyer = dict([('id', request.user.id)])
            buyer['name']                   = request.user.first_name
            buyer['surname']                = request.user.last_name
            buyer['gsmNumber']              = serializer.validated_data['phone']
            buyer['email']                  = serializer.validated_data['email']
            buyer['identityNumber']         = "00000000000"
            buyer['registrationAddress']    = serializer.validated_data['address']
            buyer['ip']                     = self.get_client_ip(request)
            buyer['city']                   = serializer.validated_data['city']
            buyer['country']                = serializer.validated_data['country']

            address = dict([('address', serializer.validated_data['address'])])
            address['country']              = serializer.validated_data['country']
            address['zipCode']              = serializer.validated_data['zip_code']
            address['contactName']          = serializer.validated_data['first_name'] + " " + serializer.validated_data['last_name']
            address['city']                 = serializer.validated_data['city']
            address['country']              = serializer.validated_data['country']

            iyzico_request = dict([('locale', 'tr')])
            iyzico_request['price']         = float(paid_amount)
            iyzico_request['paidPrice']     = float(paid_amount)
            iyzico_request['installment']   = 1
            iyzico_request['basketId']      = 2
            iyzico_request['buyer']         = buyer
            iyzico_request['callbackUrl']   = callback_url

            iyzico_request['shippingAddress']   = address
            iyzico_request['billingAddress']    = address
            iyzico_request['basketItems']       = basketItems

            iyzico_request['paymentGroup']      = 'PRODUCT'
        
            try:
                checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(iyzico_request, iyzico_options)
                decoded_response = checkout_form_initialize.read().decode('utf-8')
                json_response = json.loads(decoded_response)
                serializer.save(user=request.user,paid_amount=paid_amount,iyzico_token=json_response['token'])
                return Response(json_response,status=status.HTTP_200_OK)
            except:
                return Response({"error":"Payment form"},status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentCallbackAPIView(GenericAPIView):
    serializer_class = OrderSerializer
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')

        try:
            order = Order.objects.get(iyzico_token=token)
        except:
            return Response({"Error":"Order payment does not exists" },status=status.HTTP_400_BAD_REQUEST)
        
        iyzico_request = dict([('locale', 'tr')])
        iyzico_request['token'] = token
        iyzico_options = settings.IYZICO_OPTIONS


        try:
            checkout_form_auth = iyzipay.CheckoutForm()
            checkout_form_auth_response = checkout_form_auth.retrieve(iyzico_request, iyzico_options)
            decoded_response = checkout_form_auth_response.read().decode('utf-8')
            json_response = json.loads(decoded_response)
        
        except:
            return Response({'Error':'Check error'})
        
        if json_response["paymentStatus"] == "SUCCESS":
            order.order_status = "P"
            order.save()
        else:
            order.order_status = "E"
            order.save()
        
        """
        Redirect to frontend url
        """
        frontendURL = settings.FRONTEND_URL
        return redirect(frontendURL+"/payment-control/?token="+token)


class CheckPaymentAPIView(ListAPIView):
    queryset = Order.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class = OrderSerializer
    

    def get_queryset(self):
        paymentToken = self.kwargs['token']

        queryset = Order.objects.filter(user=self.request.user,iyzico_token=paymentToken)

        return queryset
        