from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from tts.exceptions.InvalidToken import InvalidToken

import re

class AuthenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # if request.path != '/tts/generate-text-to-voice/':
        if request.path == '/tts/login/':
            return self.get_response(request)

        pattern = re.compile(r'^Bearer\s(.+)$')
        authorization = request.headers.get('Authorization')  

        try:
            if not authorization or not pattern.match(authorization):
                raise InvalidToken
            
            token = authorization.split(' ')[-1]
            
            token_obj = AccessToken(token)
            payload = token_obj.payload
            username = payload.get('username') #user_id
            
            if not username: # verify user_id
                raise InvalidToken

        except (TokenError, InvalidToken):
            return InvalidToken().handleError() 

        return self.get_response(request)
