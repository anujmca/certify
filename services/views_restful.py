from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt


from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import SessionAuthentication, BasicAuthentication



from io import StringIO, BytesIO
from pandas import *
from generators import pptxGenerator as generator
from services.models import *
from .utilities import get_user_by_awardee


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


# region Event Views
class EventList(APIView):
    """
    List all events, or create a new event.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetail(APIView):
    """
    Retrieve, update or delete a event instance.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        event = self.get_object(pk)
        if 'template_id' in request.POST:
            template = Template.objects.get(pk=request.data['template_id'])
            event.template = template

        if 'datasheet_id' in request.POST:
            datasheet = DataSheet.objects.get(pk=request.data['datasheet_id'])
            event.datasheet = datasheet

        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# endregion


# region Template Views
class TemplateList(APIView):
    """
    List all templates, or create a new template.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        templates = Template.objects.all()
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateDetail(APIView):
    """
    Retrieve, update or delete a template instance.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Template.objects.get(pk=pk)
        except Template.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        template = self.get_object(pk)
        serializer = TemplateSerializer(template)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        template = self.get_object(pk)
        serializer = TemplateSerializer(template, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        template = self.get_object(pk)
        serializer = TemplateSerializer(template, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        template = self.get_object(pk)
        template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# endregion


# region DataSheet Views
class DataSheetList(APIView):
    """
    List all datasheets, or create a new datasheet.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        datasheets = DataSheet.objects.all()
        serializer = DataSheetSerializer(datasheets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DataSheetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DataSheetDetail(APIView):
    """
    Retrieve, update or delete a datasheet instance.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return DataSheet.objects.get(pk=pk)
        except DataSheet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        datasheet = self.get_object(pk)
        serializer = DataSheetSerializer(datasheet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        datasheet = self.get_object(pk)
        serializer = DataSheetSerializer(datasheet, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        datasheet = self.get_object(pk)
        serializer = DataSheetSerializer(datasheet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        datasheet = self.get_object(pk)
        datasheet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# endregion


# region Function Based API
@api_view(['POST'])
@csrf_exempt
def generate_certificate(request):
    event_id = request.POST.get('event_id')
    event = Event.objects.get(pk=event_id)
    if event.template is not None and event.datasheet is not None:
        # templateFile =  template.file.read()
        data_sheet_excel = ExcelFile(event.datasheet.data_sheet)
        df_awardees = data_sheet_excel.parse(data_sheet_excel.sheet_names[0])

        latest_batch_id = 0 if not Certificate.objects.exists() else Certificate.objects.order_by('-batch_id')[
            0].batch_id
        batch_id = 1 if latest_batch_id is None else latest_batch_id + 1

        awardee_count = 0
        for i, row in df_awardees.iterrows():
            awardee_count = awardee_count + 1
            data_sheet_dictionary = {}
            data_keys = []
            for key in df_awardees.columns:
                data_sheet_dictionary[key] = row[key]
                obj = DataKey(name=key, value=data_sheet_dictionary[key])
                obj.save()
                data_keys.append(obj)

            certificate_file = generator.generate(template_file_path=event.template.file,
                                                  data_sheet_dictionary=data_sheet_dictionary)
            # certificate_file.save(settings.MEDIA_ROOT + '')

            target_stream = BytesIO()
            certificate_file.save(target_stream)

            user, password = get_user_by_awardee(row)

            certificate = None
            if password is None: # existing user
                certificate = Certificate.objects.get(awardee=user, event=event)

            if certificate is None:
                certificate = Certificate(batch_id=batch_id, event=event)
            else:
                certificate.batch_id = batch_id

            certificate.save()
            certificate.awardee = user
            certificate.sms_available = False if user is None or user.profile.phone_number is None else True
            certificate.email_available = False if user is None or user.email is None else True
            certificate.data_keys.set(data_keys)
            certificate.file.save(data_sheet_dictionary['employee_name'] + '_' + str(batch_id) + '.pptx', target_stream)
            certificate.save()

            # send email here
            # if password is not None:
               # send the password also in that email

        event.awardee_count = awardee_count
        event.are_certificates_generated = True
        event.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# endregion