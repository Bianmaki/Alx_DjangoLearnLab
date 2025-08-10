# LibraryProject/middleware.py
class ContentSecurityPolicyMiddleware:
    """
    Small middleware to add a CSP header. Adjust sources as needed.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # strict policy - allow only self for scripts/styles by default
        csp = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
        response.headers['Content-Security-Policy'] = csp
        return response
