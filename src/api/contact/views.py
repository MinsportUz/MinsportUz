from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from admin_panel.model import contact, settings
from . import serializers
from .. import pagination


class CustomModalViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')

        return queryset


class ContactView(viewsets.ViewSet, CustomModalViewSet, generics.CreateAPIView):
    """
    POST: /contact/ - user sends contact here, including messages, phone_number and email.
    Some fields are required*

    POST: /contact/status/ - user sends "id_number" and "key" ONLY, response is contact information & status code
    """
    queryset = contact.ContactType.objects.all()
    serializer_class = serializers.ContactSerializer
    pagination_class = None
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        instance = contact.ContactType.objects.all()
        return Response(serializers.ContactTypeSerializer(instance, many=True).data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        if serializer.is_valid():
            obj = contact.Contact.objects.create(**serializer.validated_data)
            payload = {
                'id': obj.id_number,
                'key': obj.key,
            }
            return Response(payload, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def status(self, request, *args, **kwargs):
        data = self.request.POST.dict()
        # print(data, 'asdasda')
        try:
            obj = contact.Contact.objects.get(id_number=data['id_number'], key=data['key'])
            payload = {
                'contact': self.serializer_class(obj).data,
                'code': obj.status,
                'status': dict(contact.STATUS)
            }
            return Response(payload, status=status.HTTP_200_OK)
        except Exception:
            return Response('Object not found', status=status.HTTP_404_NOT_FOUND)


class FeedbackView(ContactView):
    queryset = contact.Feedback.objects.all()
    pagination_class = None
    http_method_names = ['get', 'post']
    serializer_class = serializers.FeedbackSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        if serializer.is_valid():
            obj = contact.Feedback.objects.create(**serializer.validated_data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class IndexContactView(CustomModalViewSet):
    queryset = contact.ContactStat.objects.all()
    serializer_class = None
    pagination_class = None
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset().last()
        payload = {
            'total': instance.total,
            'process': instance.process,
            'review': instance.review,
            'reject': instance.reject,
        }

        return Response(payload)


class ReceptionView(CustomModalViewSet):
    queryset = contact.Reception.objects.filter(active=True)
    serializer_class = serializers.ReceptionSerializer
    pagination_class = None
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.serializer_class
        obj = settings.ContactSetting.objects.last()
        payload = {
            'data': serializer(instance, many=True).data,
            'notice': obj.notice,
        }

        return Response(payload)


class GetStatsView(viewsets.ModelViewSet):
    queryset = contact.Feedback.objects.all()
    serializer_class = serializers.FeedbackSerializer
    pagination_class = pagination.VotePagination
    http_method_names = ['get']


class AdmReceptionView(viewsets.ModelViewSet):
    queryset = contact.Reception.objects.all()
    serializer_class = serializers.AdmReceptionSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated,]
    # http_method_names = ['get', 'post', 'put', 'delete']


class AdmWeekDayView(viewsets.ModelViewSet):
    queryset = contact.WeekDay.objects.all()
    serializer_class = serializers.AdmWeekDaySerializer
    pagination_class = None
    permission_classes = [IsAuthenticated,]
    # http_method_names = ['get', 'post', 'put', 'delete']


class AdmContactTypeView(viewsets.ModelViewSet):
    queryset = contact.ContactType.objects.all()
    serializer_class = serializers.AdmContactTypeSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated,]
    # http_method_names = ['get', 'post', 'put', 'delete']


class AdmContactView(viewsets.ModelViewSet):
    queryset = contact.Contact.objects.all().order_by('-created_at')
    serializer_class = serializers.AdmContactSerializer
    pagination_class = pagination.CustomPagination
    permission_classes = [IsAuthenticated,]
    # http_method_names = ['get', 'post', 'put', 'delete']

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = request.data.get('status')
        instance.save()
        return Response(self.serializer_class(instance).data)


class AdmFeedBackView(viewsets.ModelViewSet):
    queryset = contact.Feedback.objects.all().order_by('-created_at')
    serializer_class = serializers.AdmFeedbackSerializer
    pagination_class = pagination.CustomPagination
    permission_classes = [IsAuthenticated,]
    # http_method_names = ['get', 'post', 'put', 'delete']

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = request.data.get('status')
        instance.save()
        return Response(self.serializer_class(instance).data)


class AppealView(viewsets.ModelViewSet):
    queryset = contact.Contact.objects.all()
    serializer_class = serializers.AppealSerializer
    pagination_class = None
    http_method_names = ['post', ]