


class LoginMiddleware(object):



    def process_request(self, request):
        print request.path
        pass

    def process_view(self, request, callback, callback_args, callback_kwargs):
        pass

    def process_response(self, request, response):
        return response