from functools import wraps
from django.http import JsonResponse
from rest_framework import status

ACCEPTED_TOKEN = ('omni_pretest_token')

def require_access_token(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kargs):
        token = request.data.get('token')

        if not token:
            return JsonResponse({"message": "Token is required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if token != ACCEPTED_TOKEN:
            return JsonResponse({"message": "Invalid Access Token"}, status=status.HTTP_401_UNAUTHORIZED)

        return view_func(request, *args, **kargs)
    return wrapper