from .adapters.fake_you_api_adapter import FakeYouAPIAdapter
import re
import requests
import jwt
from mysite.settings import SECRET_KEY


api_adapter_fake_you = FakeYouAPIAdapter('https://api.fakeyou.com/tts/inference', 'https://api.fakeyou.com/tts/job/')


def get_audio_link(prompt, mode, voice_id):
    response = api_adapter_fake_you.get_audio_link(prompt, mode, voice_id)
    return response


def authenticate_token(request):
    pattern = re.compile(r'^Bearer\s(.+)$')
    authorization = request.headers.get('Authorization', None)

    if authorization and pattern.match(authorization):
        token = authorization.split(' ')[-1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            
            # do something 

            return True
            
        except jwt.ExpiredSignatureError:
            return False
        except jwt.DecodeError:
            return False
    
    return False


def check_authen(request):
    pattern = re.compile(r'^Bearer\s(.+)$')
    authorization = request.headers.get('Authorization', None)

    if authorization and pattern.match(authorization):
        token = authorization.split(' ')[-1]
        data={
            "token": token
        }

        response = requests.post("http://localhost:8000/api/token/verify/", json=data)

        if response.status_code == 200:
            return True
       
    return False


def verify_request(request):
    if "prompt" in request.POST and "mode" in request.POST and "voice_id" in request.POST:
        if request.POST["prompt"].strip() and request.POST["mode"] in ('0','1', 0, 1) and request.POST["voice_id"].strip():
            return {
                "result": True
            }
        else:
            return {
                "result": False,
                "status": {
                    "code": 400,
                    "message": "Bad request"
                },
                "body": {
                    "error": "Wrong input"
                }
            }
    else:
        return {
                "result": False,
                "status": {
                    "code": 400,
                    "message": "Bad request"
                },
                "body": {
                    "error": "Missing field"
                }
            }

