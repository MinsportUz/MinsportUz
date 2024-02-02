from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import ParticipantsSerializer, EvolutionCriteriaSerializer, VoteSerializer, \
    ParticipantsFilterSerializer, BotLinkSerializer, ParticipantsListSerializer, SubscribersSerializer
from admin_panel.model.rating import Vote, Participants, EvolutionCriteria, UnicalCode, Subscribers
from api.pagination import CustomPagination, VotePagination
from decouple import config
from rest_framework import status

def generate_unical_code():
    import secrets

    # Generate a short unique code
    unique_code = secrets.token_hex(4)  # 4 bytes = 8 characters
    return unique_code


class ParticipantsViewSet(ModelViewSet):
    queryset = Participants.objects.all()
    serializer_class = ParticipantsSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    pagination_class = CustomPagination

    # def get_queryset(self):
    #     queryset = self.queryset
    #     if hasattr(self.queryset.model, 'title'):
    #         queryset = self.queryset.exclude(title__exact='')
    #
    #     return queryset


class EvolutionCriteriaViewSet(ModelViewSet):
    queryset = EvolutionCriteria.objects.all()
    serializer_class = EvolutionCriteriaSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    # def get_queryset(self):
    #     queryset = self.queryset
    #     if hasattr(self.queryset.model, 'title'):
    #         queryset = self.queryset.exclude(title__exact='')
    #
    #     return queryset


class VoteViewSet(ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        unical_code = request.data.get('code', False)
        participant = request.data.get('participant', 0)
        evolution_criteria = request.data.get('evolution_criteria', 0)
        if participant == 0 or evolution_criteria == 0:
            return Response({'status': False, 'detail': 'Ma\'lumotlar yetarli emas!'},
                            status=status.HTTP_204_NO_CONTENT)

        if unical_code:
            try:
                unical_code = UnicalCode.objects.get(code=unical_code, status=True)
                subscriber = Subscribers.objects.get(unical_code=unical_code)
                if not subscriber:
                    return Response({'status': False, 'detail': 'Ovoz berishda xatolig yuzaga keldi'},
                                    status=status.HTTP_404_NOT_FOUND)
                check_vote = Vote.objects.filter(subscriber=subscriber).exists()
                if check_vote:
                    return Response({'status': False, 'detail': 'Siz avval ovoz bergansiz'},
                                    status=status.HTTP_404_NOT_FOUND)
                Vote.objects.create(
                    participant=Participants.objects.get(id=participant),
                    subscriber=subscriber,
                    evolution_criteria=EvolutionCriteria.objects.get(id=evolution_criteria),
                )
                return Response({'status': True, 'detail': 'Ovoz berildi!'}, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'status': False, 'detail': 'Kod aniqlanmadi!'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'Kod kiritilmadi!'}, status=status.HTTP_204_NO_CONTENT)


class ParticipantsFilterViewSet(ModelViewSet):
    queryset = Participants.objects.all()
    serializer_class = ParticipantsFilterSerializer
    http_method_names = ['get', 'post']
    pagination_class = VotePagination

    def create(self, request, *args, **kwargs):
        search = request.data.get('search', False)
        region = request.data.get('region', False)
        district = request.data.get('district', False)
        organization = request.data.get('organization', False)
        filters = dict()
        if search and search != '' and search != 'null':
            filters['firstname__icontains'] = search
            filters['lastname__icontains'] = search
        if region and region != '0' and region != '':
            filters['region'] = region
        if district and district != '0' and district != '':
            filters['district'] = district
        if organization and organization != '0' and organization != '':
            filters['organization'] = organization
        queryset = Participants.objects.filter(**filters)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ParticipantsListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ParticipantsListSerializer(queryset, many=True)
        return Response(serializer.data)


class BotLinkViewSet(ModelViewSet):
    queryset = Participants.objects.all()
    serializer_class = BotLinkSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        bot_username = config('BOT_USERNAME')
        unical_code = generate_unical_code()
        UnicalCode.objects.create(code=unical_code, status=True)
        return Response({'link': f'https://t.me/{bot_username}?start={unical_code}', 'code': unical_code},
                        status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        unical_code = request.data.get('code', 0)
        if unical_code:
            try:
                unical_code = UnicalCode.objects.get(code=unical_code, status=True)
                subscriber = Subscribers.objects.filter(unical_code=unical_code)
                if not subscriber.exists():
                    return Response({'status': False, 'detail': "Kanalga a'zolik aniqlanmadi"},
                                    status=status.HTTP_204_NO_CONTENT)

                return Response({'status': True, 'detail': 'Success'}, status=status.HTTP_200_OK)
            except UnicalCode.DoesNotExist:
                return Response({'status': False, 'detail': 'Error'}, status=status.HTTP_204_NO_CONTENT)


class SubscribersViewSet(ModelViewSet):
    queryset = Subscribers.objects.all()
    serializer_class = SubscribersSerializer
    http_method_names = ['get', 'post', ]
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        chat_id = request.data.get('chat_id', 0)
        if chat_id == 0 or chat_id.isdigit() is False:
            return Response({'status': False, 'detail': "Xatolik"}, status=status.HTTP_204_NO_CONTENT)
        subscriber = Subscribers.objects.filter(chat_id=int(chat_id))
        if not subscriber.exists():
            return Response({'status': False, 'detail': "Xatolik"}, status=status.HTTP_204_NO_CONTENT)
        return Response({'status': True, 'detail': 'Success'}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        unical_code = request.data.get('code', None)
        chat_id = request.data.get('chat_id', 0)
        fullname = request.data.get('fullname', None)
        if chat_id == str(0):
            return Response({'status': False, 'detail': "Xatolik"}, status=status.HTTP_204_NO_CONTENT)
        if unical_code is None:
            _unical_code = generate_unical_code()
            unical_code = UnicalCode.objects.create(code=_unical_code, status=True)
        else:
            unical_code = UnicalCode.objects.filter(code=unical_code, status=True).first()
        subscriber = Subscribers.objects.filter(chat_id=chat_id)
        if not subscriber.exists():
            Subscribers.objects.create(unical_code=unical_code, chat_id=chat_id, fullname=fullname)
            return Response({'status': True, 'detail': 'Success'}, status=status.HTTP_200_OK)
        subscriber = subscriber.first()
        if subscriber.unical_code != unical_code and unical_code is not None:
            subscriber.unical_code = unical_code
            subscriber.fullname = fullname
            subscriber.save()
        return Response({'status': True, 'detail': 'Success'}, status=status.HTTP_200_OK)
