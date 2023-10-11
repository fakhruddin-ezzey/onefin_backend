from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        header_to_check = dict(request.headers)

        if 'Authorization' not in header_to_check.keys():
            jwt_token_missing_response = Response({'authentication_error':'Token Authentication is not enforced. Please make sure Bearer is applied'})
            jwt_token_missing_response.accepted_renderer = JSONRenderer()
            jwt_token_missing_response.accepted_media_type = "application/json"
            jwt_token_missing_response.renderer_context = {}
            jwt_token_missing_response.render()

            return jwt_token_missing_response
        
        
        
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        print("response_type: ", type(response))
        print("response: ", type(response))

        # Code to be executed for each request/response after
        # the view is called.

        return response