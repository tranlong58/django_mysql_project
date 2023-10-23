from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import jwt
import datetime
from django.utils import timezone
from mysite.settings import SECRET_KEY

from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


from .services import tts_services

# Create your views here.


def index(request):
    return render(request, "tts/index.html")


def result(request):
    audio_link = request.session.get("audio_link", None)

    if audio_link is not None:
        context = {"audio_link": audio_link}
        del request.session["audio_link"]
    else:
        context = {}

    return render(request, "tts/result.html", context)


def solve(request):
    prompt = request.POST["prompt"]
    mode = request.POST["mode"]
    voice_id = request.POST["voice_id"]

    response = tts_services.get_audio_link(prompt, mode, voice_id)

    request.session["audio_link"] = response.get("body").get("audio_link", None)

    return HttpResponseRedirect(reverse("tts:result"))


# @csrf_exempt
# def create_token(request):
#     expiration_time = timezone.now() + datetime.timedelta(hours=1)
#     exp_timestamp = expiration_time.timestamp()

#     payload = request.POST.copy()
#     payload['exp'] = exp_timestamp

#     token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

#     response = {
#         "token": token
#     }

#     return JsonResponse(response)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        token = RefreshToken()
        
        payload = {}
        for key, value in request.data.items():
            if isinstance(value, list) and len(value) == 1:
                payload[key] = value[0]
            else:
                payload[key] = value

        token.payload.update(payload)

        tokens = {
            'access': str(token.access_token),
            'refresh': str(token)
        }

        return JsonResponse(tokens, status=200)


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
            # if user_id:
            #     return JsonResponse({'result': True, 'message': 'success'})
            # else:
            #     return JsonResponse({'result': False, 'message': 'fail'})

            return JsonResponse({'result': True, 'message': 'success'})

        except TokenError:
            return JsonResponse({'result': False, 'message': 'Token is invalid'})


@csrf_exempt
def get_audio_api(request):
    if tts_services.check_authen(request):
        response = tts_services.verify_request(request)

        if response["result"]:
            prompt = request.POST["prompt"]
            mode = request.POST["mode"]
            voice_id = request.POST["voice_id"]
            voice_volume = request.POST.get("voice_volume", None)
            pitch = request.POST.get("pitch", None)
            speech = request.POST.get("speech", None)
            
            response = tts_services.get_audio_link(prompt, mode, voice_id, voice_volume, pitch, speech)
    else:
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
        
    return JsonResponse(response, status=response['status']['code'])