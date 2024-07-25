from django.http import HttpResponseForbidden


class RestrictAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info.lstrip("/")
        if (
            path.startswith("media/colivings/")
            or path.startswith("media/profiles/")
            or path.startswith("media/user_reports/")
        ):
            if not request.user.is_staff:
                return HttpResponseForbidden()
        return self.get_response(request)
