from courses.models import CustomUser

class CustomUserMiddleware():
    def process_request(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated():
            request.user.__class__ = CustomUser