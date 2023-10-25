from django.http import JsonResponse

class InvalidToken(BaseException):
    def __init__(self, message="Invalid token", code=401):
        self.message = message
        self.code = code
        super().__init__(self.message)
    

    def handleError(self):
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

        return JsonResponse(response, status=401)