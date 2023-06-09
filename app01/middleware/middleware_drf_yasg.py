class AddAuthorizationHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = "VUlrSPfoIopryuzZxf8WuHTmQmUlfKxyz6Ja1iuIjCYBtg8aTsrRE1FqsBYwSHfs"
        request.headers["Authorization"] = f"Bearer {token}"
        return self.get_response(request)