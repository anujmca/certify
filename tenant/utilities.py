from .models import Client

def get_hostname(request):
    return request.get_host().split(':')[0].lower()


def get_tenant(request):
    hostname = get_hostname(request)
    subdomain = hostname.split('.')[0]
    # return Client.objects.filter(subdomain=subdomain).first()
    return Client.objects.first()
