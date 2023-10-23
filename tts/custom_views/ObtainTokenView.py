from django.http import JsonResponse

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        token = RefreshToken()
        
        payload = request.POST
       
        token.payload.update(payload)

        tokens = {
            'access': str(token.access_token),
            'refresh': str(token)
        }

        return JsonResponse(tokens, status=200)