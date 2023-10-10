from .adapters.fake_you_api_adapter import FakeYouAPIAdapter

api_adapter = FakeYouAPIAdapter('https://api.fakeyou.com/tts/inference', 'https://api.fakeyou.com/tts/job/')


def get_audio_link(prompt, mode, voice_id):
    result_job_token = api_adapter.make_tts_request(prompt, mode, voice_id)
    response = api_adapter.poll_tts_request_status(result_job_token)

    return response
  

