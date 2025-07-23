from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .services import lipa_na_mpesa_online
from .models import MpesaPayment
from store.models import Order

class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        phone_number = request.user.phone_number

        if not all([order_id, phone_number]):
            return Response({"error": "Order ID is required and you must have a phone number on your profile."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            order = Order.objects.get(id=order_id, buyer=request.user, status=Order.OrderStatus.PENDING)
            amount = order.total_price
            
            mpesa_response = lipa_na_mpesa_online(phone_number, amount, order_id)
            
            if mpesa_response.get("ResponseCode") == "0":
                MpesaPayment.objects.create(
                    order=order,
                    amount=amount,
                    phone_number=phone_number,
                    description=mpesa_response.get("ResponseDescription"),
                    checkout_request_id=mpesa_response['CheckoutRequestID']
                )
                return Response({"message": "STK push initiated successfully. Please check your phone."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": mpesa_response.get("errorMessage", "An error occurred.")}, status=status.HTTP_400_BAD_REQUEST)

        except Order.DoesNotExist:
            return Response({"error": "Pending order with that ID not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MpesaCallbackView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        stk_callback = data.get('Body', {}).get('stkCallback', {})
        checkout_request_id = stk_callback.get('CheckoutRequestID')
        result_code = stk_callback.get('ResultCode')

        if not checkout_request_id:
            return Response({"error": "Invalid callback data"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payment = MpesaPayment.objects.get(checkout_request_id=checkout_request_id)
            order = payment.order

            if result_code == 0:
                payment.status = MpesaPayment.PaymentStatus.COMPLETED
                order.status = Order.OrderStatus.PAID
                for item in order.items.all():
                    item.animal.is_sold = True
                    item.animal.save()
            else:
                payment.status = MpesaPayment.PaymentStatus.FAILED
                order.status = Order.OrderStatus.FAILED

            payment.save()
            order.save()
            return Response({"message": "Callback processed"}, status=status.HTTP_200_OK)
        
        except MpesaPayment.DoesNotExist:
            return Response({"error": "Payment record not found"}, status=status.HTTP_404_NOT_FOUND)