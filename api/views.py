from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Order

ACCEPTED_TOKEN = ('omni_pretest_token')


@api_view(['POST'])
def import_order(request):
    token = request.data.get('token')

    if not token:
        return JsonResponse({"message": "Token is required"}, status=status.HTTP_401_UNAUTHORIZED)
    
    if token != ACCEPTED_TOKEN:
        return JsonResponse({"message": "Invalid Access Token"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # check if order_number and total_price exists
    if not request.data.get('order_number'):
        return JsonResponse({"message": "Order number is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not request.data.get('total_price'):
        return JsonResponse({"message": "Total price is required"}, status=status.HTTP_400_BAD_REQUEST)

    if not isinstance(request.data.get('order_number'), int):
        return JsonResponse({"message": "Order number must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

    if not isinstance(request.data.get('total_price'), int):
        return JsonResponse({"message": "Total price must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

    order_number = request.data.get('order_number')
    total_price = request.data.get('total_price')

    order = Order.objects.create(
        order_number=order_number,
        total_price=total_price,
    )

    return JsonResponse({"message": "Order imported successfully", "order_id": order.id, "order_number": order.order_number, "total_price": order.total_price})