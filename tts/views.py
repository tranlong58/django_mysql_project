from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed


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
def get_audio_api(request):
    if tts_services.check_authen(request):
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
    