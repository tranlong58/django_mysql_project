from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.http import JsonResponse

import re


class AuthenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/tts/login/':
            return self.get_response(request)
        
        is_authenticated = True

        pattern = re.compile(r'^Bearer\s(.+)$')
        authorization = request.headers.get('Authorization')  

        if authorization and pattern.match(authorization):
            token = authorization.split(' ')[-1]

            try:
                token_obj = AccessToken(token)
                payload = token_obj.payload
                username = payload.get('username') #user_id
                # todo something with user_id
                
            except TokenError:
                is_authenticated = False

        else:
            is_authenticated = False
        

        if not is_authenticated:
            response = {
                "result": False,
                "status": {
                    "code": 401,
                    "message": "Authentication error"
                },
                "body": {
                    "error": "Token is invalid or expired"
                }
            }

            return JsonResponse(response, status=401)
        
        else:
            return self.get_response(request)
