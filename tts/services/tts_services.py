from .adapters.fake_you_api_adapter import FakeYouAPIAdapter
import re
import requests

api_adapter_fake_you = FakeYouAPIAdapter('https://api.fakeyou.com/tts/inference', 'https://api.fakeyou.com/tts/job/')


def get_audio_link(request):
    prompt = request.POST["prompt"]
    mode = request.POST["mode"]
    voice_id = request.POST["voice_id"]
    voice_volume = request.POST.get("voice_volume", None)
    pitch = request.POST.get("pitch", None)
    speech = request.POST.get("speech", None)

    if mode == 0 or mode == '0':
        response = api_adapter_fake_you.get_audio_link_simple(prompt, voice_id)
    else:
        response = api_adapter_fake_you.get_audio_link_advance(prompt, voice_id, voice_volume, pitch, speech)
    
    return response


def check_authen(request):
    pattern = re.compile(r'^Bearer\s(.+)$')
    authorization = request.headers.get('Authorization')

    if authorization and pattern.match(authorization):
        token = authorization.split(' ')[-1]
        data = {
            "token": token
        }

        response = requests.post("http://localhost:8000/tts/verify-token/", json=data)

        if response.json().get('result'):
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

