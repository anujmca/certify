from .models import Client,  Domain

def get_hostname(request):
    return request.get_host().split(':')[0].lower()


def get_tenant(request):
    hostname = get_hostname(request)
    subdomain = hostname.split('.')[0]

    matching_domains = [d for d in Domain.objects.all() if d.subdomain == subdomain]
    return None if not matching_domains else matching_domains[0].tenant
