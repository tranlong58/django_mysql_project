from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from tts.services import tts_services

# Create your views here.


@csrf_exempt
def get_audio_api(request):
    is_valid_input = tts_services.verify_input(request)

    if is_valid_input:
        response = tts_services.get_audio_link(request)
    else:
        response = {
            "result": False,
            "status": {
                "code": 400,
                "message": "Bad request"
            },
            "body": {
                "error": "Missing field or Wrong input"
            }
        }
        
    return JsonResponse(response, status=response['status']['code'])