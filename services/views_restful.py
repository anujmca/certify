from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt


from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import Group


from io import StringIO, BytesIO
from generators import pptxGenerator as generator
from .utilities import *
from django.db.models import Q
from services.models import *
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
import services.utilities as utl

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

# region Utilities
def get_user_by_awardee(request, df_awardee):
    phone = df_awardee[BaseToken.phone_number]
    email = df_awardee[BaseToken.email_id]
    email = email if is_valid_email(email) else None

    user = get_user_by_email_or_phone(email, phone)
    password = None

    if user is None:
        user_name = email if email else phone if phone else None
        if user_name and isinstance(user_name, str):
            password = User.objects.make_random_password() if settings.IS_HARDCODED_PASSWORD_GENERATED == False else 'Gurgaon1'
            user = User.objects.create_user(username=user_name, password=password)
            if email is not None:
                user.email = email
            user.first_name = df_awardee[BaseToken.first_name]
            user.last_name = df_awardee[BaseToken.last_name]

            # user.groups = [Group.objects.get(name=utl.Groups.awardee)]
            awardee_group = Group.objects.get(name=utl.Groups.awardee)
            if user.groups:
                user.groups.add(awardee_group)
            else:
                user.groups = [awardee_group]
            user.save()
            profile = Profile.objects.create(user=user)
            Profile.created_by = request.user
            profile.phone_number = phone
            profile.client_user_id = df_awardee[BaseToken.id]
            profile.save()
            user.save()

    return user, password

def get_user_by_email_or_phone(email, phone):
    try:
        return User.objects.get(Q(email=email) | Q(profile__phone_number=phone))
    except User.DoesNotExist:
        return None
# endregion

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

    # @login_required
    # @allowed_users(allowed_roles=[utl.Groups.issuer])
    def get(self, request, format=None):
        templates = Template.objects.all()
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data)

    # @login_required
    # @allowed_users(allowed_roles=[utl.Groups.issuer])
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

    # @login_required
    # @allowed_users(allowed_roles=[utl.Groups.issuer])
    def get(self, request, pk, format=None):
        template = self.get_object(pk)
        serializer = TemplateSerializer(template)
        return Response(serializer.data)

    # @login_required
    # @allowed_users(allowed_roles=[utl.Groups.issuer])
    def put(self, request, pk, format=None):
        template = self.get_object(pk)
        serializer = TemplateSerializer(template, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @login_required
    # @allowed_users(allowed_roles=[utl.Groups.issuer])
    def patch(self, request, pk, format=None):
        template = self.get_object(pk)
        serializer = TemplateSerializer(template, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @login_required
    # @allowed_users(allowed_roles=[utl.Groups.issuer])
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

    # @login_required
    # @allowed_users(allowed_roles=[utl.Groups.issuer])
    def get(self, request, format=None):
        datasheets = DataSheet.objects.all()
        serializer = DataSheetSerializer(datasheets, many=True)
        return Response(serializer.data)

    # @login_required
    # @allowed_users(allowed_roles=[utl.Groups.issuer])
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

    # @login_required
    # @allowed_users(allowed_roles=[utl.Groups.issuer])
    def get(self, request, pk, format=None):
        datasheet = self.get_object(pk)
        serializer = DataSheetSerializer(datasheet)
        return Response(serializer.data)

    # @login_required
    # @allowed_users(allowed_roles=[utl.Groups.issuer])
    def put(self, request, pk, format=None):
        datasheet = self.get_object(pk)
        serializer = DataSheetSerializer(datasheet, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @login_required
    # @allowed_users(allowed_roles=[utl.Groups.issuer])
    def patch(self, request, pk, format=None):
        datasheet = self.get_object(pk)
        serializer = DataSheetSerializer(datasheet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @login_required
    # @allowed_users(allowed_roles=[utl.Groups.issuer])
    def delete(self, request, pk, format=None):
        datasheet = self.get_object(pk)
        datasheet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# endregion


# region Function Based API
@login_required
@allowed_users(allowed_roles=[utl.Groups.issuer])
@api_view(['POST'])
# @csrf_exempt
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

            user, password = get_user_by_awardee(request, row)

            certificate = None
            if user is not None and password is None: # existing user
                try:
                    certificate = Certificate.objects.get(awardee=user, event=event)
                except:
                    certificate = None

            if certificate is None:
                certificate = Certificate(batch_id=batch_id, event=event)
            else:
                certificate.batch_id = batch_id

            certificate.save()
            certificate.awardee = user
            certificate.sms_available = False if user is None or user.profile.phone_number is None else True
            certificate.email_available = False if user is None or user.email is None else True
            certificate.data_keys.set(data_keys)
            certificate_file_name = f'{data_sheet_dictionary[BaseToken.first_name]}' \
                                    f'_{data_sheet_dictionary[BaseToken.last_name]}' \
                                    f'_{event.id}_{batch_id}.pptx'

            # certificate.file.save(data_sheet_dictionary['employee_name'] + '_' + str(batch_id) + '.pptx', target_stream)
            certificate.file.save(certificate_file_name, target_stream)
            certificate.save()

            # send email here
            # if password is not None:
               # send the password also in that email

        event.awardee_count = awardee_count
        event.are_certificates_generated = True
        event.save()
        data = {'id': event.id, 'result': 'success'}
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        data = {'id': event.id, 'result': 'failure'}
        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# endregion