from .adapters.fake_you_api_adapter import FakeYouAPIAdapter

api_adapter_fake_you = FakeYouAPIAdapter('https://api.fakeyou.com/tts/inference', 'https://api.fakeyou.com/tts/job/')


def get_audio_link(prompt, mode, voice_id):
    response = api_adapter_fake_you.get_audio_link(prompt, mode, voice_id)
    return response


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

