from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

import requests
import uuid
import time

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

def wait_for_tts_complete(get_audio_path_url):
    while True:
        response_new = requests.get(get_audio_path_url)
        if response_new.status_code != 200:
            return None  

        state = response_new.json().get('state')
        status = state.get('status')

        if status == 'complete_success':
            return state.get('maybe_public_bucket_wav_audio_path')
        elif status == 'complete_failure' or status == 'dead':
            return None  

        time.sleep(0.5)

def solve(request):
    body_request = {
        "prompt": request.POST["prompt"],
        "mode": request.POST["mode"],
        "voice_id": request.POST["voice_id"],
    }
    
    tts_url = 'https://api.fakeyou.com/tts/inference'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    uuid_idempotency_token = str(uuid.uuid4())
    data = {
        "uuid_idempotency_token": uuid_idempotency_token,
        "tts_model_token": body_request["voice_id"],
        "inference_text": body_request["prompt"],
    }

    response = requests.post(tts_url, headers=headers, json=data)

    if response.status_code == 200:
        inference_data = response.json()
        inference_job_token = inference_data.get("inference_job_token")

        get_audio_path_url = 'https://api.fakeyou.com/tts/job/' + inference_job_token
        audio_path = wait_for_tts_complete(get_audio_path_url)

        if audio_path:
            request.session["audio_path"] = audio_path

        return HttpResponseRedirect(reverse("tts:result"))
    else:
        return HttpResponseRedirect(reverse("tts:result"))