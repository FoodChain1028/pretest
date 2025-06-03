from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Order, Product
from .decorators import require_access_token

@api_view(['POST'])
@require_access_token
def import_order(request):
    # check validity of user_id    
    user_id = request.data.get('user_id')
    if not user_id:
        return JsonResponse({"message": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return JsonResponse({"message": "User ID must be an number"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"message": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST)

    # check if order_number and total_price exists
    if not request.data.get('order_number'):
        return JsonResponse({"message": "Order number is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not request.data.get('total_price'):
        return JsonResponse({"message": "Total price is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # validate products
    product_ids = request.data.get('product_ids', [])
    if not product_ids:
        return JsonResponse({"message": "At least one product is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        product_ids = [int(pid) for pid in product_ids]
    except (TypeError, ValueError):
        return JsonResponse({"message": "Product IDs must be numbers"}, status=status.HTTP_400_BAD_REQUEST)

    # Verify all products exist
    products = Product.objects.filter(id__in=product_ids)
    if len(products) != len(product_ids):
        return JsonResponse({"message": "One or more products not found"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        order_number = int(request.data.get('order_number'))
    except (TypeError, ValueError):
        return JsonResponse({"message": "Order number must be an number"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        total_price = int(request.data.get('total_price'))
    except (TypeError, ValueError):
        return JsonResponse({"message": "Total price must be an number"}, status=status.HTTP_400_BAD_REQUEST)

    # check if the total price is correct
    calculated_sum_of_product_prices = sum(p.price for p in products)
    if calculated_sum_of_product_prices != total_price:
        return JsonResponse({"message": f"Total price is incorrect. Calculated sum {calculated_sum_of_product_prices} does not match provided total price {total_price}."}, status=status.HTTP_400_BAD_REQUEST)

    order = Order.objects.create(
        user=user,
        order_number=order_number,
        total_price=total_price,
    )

    order.products.add(*products)
    
    # Prepare product details for response
    product_details = [{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price
    } for product in products]

    return JsonResponse({
        "message": "Order imported successfully", 
        "order_id": order.id, 
        "order_number": order.order_number, 
        "total_price": order.total_price,
        "created_time": order.created_time.isoformat(),
        "products": product_details
    })