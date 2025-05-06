# from corsheaders.middleware import CorsMiddleware

# class DynamicCorsMiddleware(CorsMiddleware):
#     print('hello4')
#     def process_request(self, request):
#         origin = request.META.get("HTTP_ORIGIN")
#         print('origin:',origin)
#         if origin and AllowedDomain.objects.filter(domain=origin).exists():
#             request._cors_origin_whitelist = [origin]
#         return super().process_request(request)


from django.utils.deprecation import MiddlewareMixin
from userAuth.models import Service ,AllowedHost

# class DynamicCorsMiddleware(MiddlewareMixin):
#     def process_response(self, request, response):
#         origin = request.META.get("HTTP_ORIGIN")
#         api_key = request.headers.get("X-API-KEY")
#         print('origin:', origin)
#         print('api_key:', api_key)
#         print('requet',request.headers)

#         if origin and api_key:
#             try:
#                 service = Service.objects.get(public_key=api_key)
#                 if AllowedHost.objects.filter(service=service, domain=origin).exists():
#                     print('hello5')
#                     response["Access-Control-Allow-Origin"] = origin
#                     response["Access-Control-Allow-Headers"] = "X-API-KEY, Content-Type"
#                     response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
#             except Service.DoesNotExist:
#                 print("Service not found for the provided API key.")
#                 pass

#         return response

class DynamicCorsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        origin = request.META.get("HTTP_ORIGIN")
        api_key = request.headers.get("X-API-KEY")
        # print('origin:', origin)
        # print('api_key:', api_key)

        if origin:
            try:
                if AllowedHost.objects.filter( domain=origin).exists():
                    response["Access-Control-Allow-Origin"] = origin
                    response["Access-Control-Allow-Headers"] = "X-API-KEY, Content-Type"
                    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                else:
                    print('no domain')
            except Service.DoesNotExist:
                print("Service not found for the provided API key.")
                pass

        return response

# class DynamicCorsMiddleware(MiddlewareMixin):
#     def process_response(self, request, response):
#         origin = request.META.get("HTTP_ORIGIN")
#         api_key = request.headers.get("X-API-KEY")

#         host =  AllowedHost.objects.first()
#         print('host:', host.domain)
#         print('origin:', origin)
#         print('api_key:', api_key)

#         if origin:    
#             response["Access-Control-Allow-Origin"] = origin
#             response["Access-Control-Allow-Headers"] = "X-API-KEY, Content-Type"
#             response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                
#         return response
