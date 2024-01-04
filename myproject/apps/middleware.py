from django.utils.deprecation import MiddlewareMixin


class XFrameOptionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response["X-Frame-Options"] = "SAMEORIGIN"  # 设置 X-Frame-Options 为 SAMEORIGIN
        return response
