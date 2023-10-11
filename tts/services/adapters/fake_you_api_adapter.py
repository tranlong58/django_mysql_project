import requests
import uuid

import time

class FakeYouAPIAdapter:
    def __init__(self, make_request_url, poll_request_status_base_url):
        self.make_request_url = make_request_url
        self.poll_request_status_base_url = poll_request_status_base_url


    def make_tts_request(self, prompt, mode, voice_id):
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

        response = requests.post(self.make_request_url, headers=headers, json=data)
        
        result = {}
        if response.status_code == 200:
            result["success"] = True
            result["body"] = {
                "inference_job_token": response.json().get("inference_job_token")
            }
        else:
            result["success"] = False
            result["body"] = {
                "error": "Not found model"
            }

        return result


    def wait_for_tts_complete(self, poll_request_status_url):
        t=0
        while t<=10:
            response_new = requests.get(poll_request_status_url)
            if response_new.status_code != 200:
                return None  

            state = response_new.json().get('state')
            status = state.get('status')

            if status == 'complete_success':
                return state.get('maybe_public_bucket_wav_audio_path')
            elif status == 'complete_failure' or status == 'dead':
                return None  
            
            t+=1
            time.sleep(2)


    def poll_tts_request_status(self, result_job_token):
        if result_job_token["success"]:
            inference_job_token = result_job_token["body"].get("inference_job_token")

            audio_path = self.wait_for_tts_complete(self.poll_request_status_base_url + inference_job_token)
            
            response = {}
            if audio_path is not None:
                audio_link = "https://storage.googleapis.com/vocodes-public" + audio_path

                response = {
                    "result": True,
                    "status": {
                        "code": 200,
                        "message": "Success"
                    },
                    "body": {
                        "audio_link": audio_link
                    }
                }
            else:
                response = {
                    "result": False,
                    "status": {
                        "code": 500,
                        "message": "Not implemented"
                    },
                    "body": {
                        "error": "Audio processing failed"
                    }
                }            
        else:
            response = {
                "result": False,
                "status": {
                    "code": 400,
                    "message": "Bad request"
                },
                "body": {
                    "error": result_job_token["body"].get("error")
                }
            }
        
        return response
    
    
    def get_audio_link(self, prompt, mode, voice_id):
        result_job_token = self.make_tts_request(prompt, mode, voice_id)
        response = self.poll_tts_request_status(result_job_token)

        return response