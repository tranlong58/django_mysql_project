from django.http import JsonResponse

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Query user on database
        if username and password:
            token = AccessToken()
            token.payload.update({'username': username}) # user_id

            response = {
                'message': 'login success',
                'access': str(token),
            }

        else:
            response = {
                'message': 'login fail',
                'access': 'null',
            }

        return JsonResponse(response)