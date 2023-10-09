from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

import time

from .services import tts_services

# Create your views here.


def index(request):
    return render(request, "tts/index.html")


def result(request):
    audio_path = request.session.get("audio_path", None)

    if audio_path is not None:
        context = {"audio_path": audio_path}
        del request.session["audio_path"]
    else:
        context = {}

    return render(request, "tts/result.html", context)


def solve(request):
    prompt = request.POST["prompt"]
    mode = request.POST["mode"]
    voice_id = request.POST["voice_id"]

    response = tts_services.get_inference_job_token(prompt, mode, voice_id)

    time.sleep(0.5)

    audio_path = tts_services.get_audio_path(response)

    if audio_path is not None:
        request.session["audio_path"] = audio_path

    return HttpResponseRedirect(reverse("tts:result"))

    