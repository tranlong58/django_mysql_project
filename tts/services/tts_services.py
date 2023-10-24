from .adapters.FakeYouAPIAdapter import FakeYouAPIAdapter

api_adapter_fake_you = FakeYouAPIAdapter('https://api.fakeyou.com/tts/inference', 'https://api.fakeyou.com/tts/job/')


def get_audio_link(request):
    prompt = request.POST["prompt"]
    mode = request.POST["mode"]
    voice_id = request.POST["voice_id"]
    voice_volume = request.POST.get("voice_volume", None)
    pitch = request.POST.get("pitch", None)
    speech = request.POST.get("speech", None)

    if mode in ('0', 0):
        response = api_adapter_fake_you.get_audio_link_simple(prompt, voice_id)
    else:
        response = api_adapter_fake_you.get_audio_link_advance(prompt, voice_id, voice_volume, pitch, speech)
    
    return response


def verify_input(request):
    if not("prompt" in request.POST) or not("mode" in request.POST) or not("voice_id" in request.POST):
        return False
    
    if not request.POST["prompt"].strip() or request.POST["mode"] not in ('0','1', 0, 1) or not request.POST["voice_id"].strip():
        return False

    return True   

