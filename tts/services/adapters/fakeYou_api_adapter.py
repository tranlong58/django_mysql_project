import requests
import uuid

class FakeYouAPIAdapter:
    def get_inference_job_token(self, prompt, mode, voice_id):
        inference_job_token_url = 'https://api.fakeyou.com/tts/inference'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        uuid_idempotency_token = str(uuid.uuid4())
        data = {
            "uuid_idempotency_token": uuid_idempotency_token,
            "tts_model_token": voice_id,
            "inference_text": prompt,
        }

        response = requests.post(inference_job_token_url, headers=headers, json=data)
        return response


    def wait_for_tts_complete(self, get_audio_path_url):
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


    def get_audio_path(self, response):
        if response.status_code == 200:
            inference_data = response.json()
            inference_job_token = inference_data.get("inference_job_token")

            get_audio_path_url = 'https://api.fakeyou.com/tts/job/' + inference_job_token
            audio_path = self.wait_for_tts_complete(get_audio_path_url)

            return audio_path
        else:
            return None