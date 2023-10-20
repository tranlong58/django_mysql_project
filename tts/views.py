from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import jwt
import datetime
from django.utils import timezone
from mysite.settings import SECRET_KEY


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


@csrf_exempt
def create_token(request):
    user_id = request.POST['user_id']
    expiration_time = timezone.now() + datetime.timedelta(hours=1)
    exp_timestamp = expiration_time.timestamp()

    payload = {
        'user_id': user_id,
        'exp': exp_timestamp,
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    response = {
        "token": token
    }

    return JsonResponse(response)


@csrf_exempt
def get_audio_api(request):
    if tts_services.authenticate_token(request):
        response = tts_services.verify_request(request)

        if response["result"]:
            prompt = request.POST["prompt"]
            mode = request.POST["mode"]
            voice_id = request.POST["voice_id"]
            
            response = tts_services.get_audio_link(prompt, mode, voice_id)
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