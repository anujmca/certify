from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    # paid_until =  models.DateField()
    # on_trial = models.BooleanField()
    # created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    @property
    def subdomain(self):
        return self.domain.split('.')[0]

    def get_subdomain(self):
        return self.domain.split('.')[0]

    def __str__(self):
        return self.domain