import uuid

USER_KEY = 'uid'
TEN_YEARS = 60 * 60 * 24 * 365 * 10


def generate_uid(request):
    try:
        uid = request.COOKIES[USER_KEY]
    except KeyError:
        uid = uuid.uuid4().hex
    return uid


class UserIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        uid = generate_uid(request)
        request.uid = uid
        response = self.get_response(request)
        response.set_cookie(USER_KEY, uid, max_age=TEN_YEARS, httponly=True)
        return response
