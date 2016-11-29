

from dongnaoApi.settings import LOGIN_CHECK

from django.http.response import JsonResponse

class LoginMiddleware(object):



    def process_request(self, request):
        path = request.path
        print path,LOGIN_CHECK
        if path in LOGIN_CHECK:
            print 1111
            for key, value in request.session.items():
                print key + ' : ' + str(value)
            user_id = request.COOKIES.get('user', '')
            print user_id
            if user_id:
                return None
            else:
                return JsonResponse(dict(
                    error='please login',
                    noLogin= True
                ))
        else:
            return None

    def process_view(self, request, callback, callback_args, callback_kwargs):
        pass

    def process_response(self, request, response):
        return response
