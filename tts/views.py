from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from tts.services import tts_services

# Create your views here.


@csrf_exempt
def get_audio_api(request):
    if tts_services.check_authen(request):
        response = tts_services.verify_request(request)

        if response["result"]:
            response = tts_services.get_audio_link(request)
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