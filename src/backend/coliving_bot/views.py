from django.http import HttpResponse, HttpResponseForbidden


def media_access(request, path):
    if _check_permissions(path, request):
        response = HttpResponse()
        del response["Content-Type"]
        response["X-Accel-Redirect"] = "/protected/media/" + path
        return response
    else:
        return HttpResponseForbidden("Not authorized to access this media.")


def _check_permissions(path, request):
    if request.user.is_staff:
        return True
    if path.startswith("materials/"):
        return True
    return False
