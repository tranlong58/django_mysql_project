from .adapters.fakeYou_api_adapter import FakeYouAPIAdapter

api_adapter = FakeYouAPIAdapter()

def get_inference_job_token(prompt, mode, voice_id):
    response = api_adapter.get_inference_job_token(prompt, mode, voice_id)
    return response

def get_audio_path(response):
    audio_path = api_adapter.get_audio_path(response)
    return audio_path
