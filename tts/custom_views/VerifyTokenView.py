from django.http import JsonResponse

from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')  

        if not token:
            return JsonResponse({'result': False, 'message': 'Token is missing'})

        try:
            token_obj = AccessToken(token)
            payload = token_obj.payload
            user_id = payload.get('user_id')
            
            # todo something with user_id

            return JsonResponse({'result': True, 'message': 'success'})

        except TokenError:
            return JsonResponse({'result': False, 'message': 'Token is invalid'})