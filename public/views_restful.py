from common.views import CsrfExemptSessionAuthentication
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


# region Template Views
class PublicCertificateList(APIView):
    """
    List all templates, or create a new template.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    # @login_required
    # @allowed_users(allowed_roles=[utl.Groups.issuer])
    def get(self, request, format=None):
        templates = PublicCertificate.objects.all()
        serializer = PublicCertificateSerializer(templates, many=True)
        return Response(serializer.data)

    # # @login_required
    # # @allowed_users(allowed_roles=[utl.Groups.issuer])
    # def post(self, request, format=None):
    #     serializer = PublicCertificateSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(created_by=request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicCertificateDetail(APIView):
    """
    Retrieve, update or delete a template instance.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return PublicCertificate.objects.get(pk=pk)
        except PublicCertificate.DoesNotExist:
            raise Http404

    # @login_required
    # @allowed_users(allowed_roles=[utl.Groups.issuer])
    def get(self, request, pk, format=None):
        template = self.get_object(pk)
        serializer = PublicCertificateSerializer(template)
        return Response(serializer.data)

    # # @login_required
    # # @allowed_users(allowed_roles=[utl.Groups.issuer])
    # def put(self, request, pk, format=None):
    #     template = self.get_object(pk)
    #     serializer = PublicCertificateSerializer(template, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(updated_by=request.user)
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # # @login_required
    # # @allowed_users(allowed_roles=[utl.Groups.issuer])
    # def patch(self, request, pk, format=None):
    #     template = self.get_object(pk)
    #     serializer = PublicCertificateSerializer(template, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save(updated_by=request.user)
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # # @login_required
    # # @allowed_users(allowed_roles=[utl.Groups.issuer])
    # def delete(self, request, pk, format=None):
    #     template = self.get_object(pk)
    #     template.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
# endregion

