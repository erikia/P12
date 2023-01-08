from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from epic_events.permissions import IsAssigneeOrReadOnlyPermission, IsSalesOrReadOnlyPermission
from account.serializers import AccountSerializer
from account.models import Account
from contract.models import Contract
from contract.serializers import ContractSerializer
from event.models import Event
from event.serializers import EventSerializer
import logging

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='app.log',
                    filemode='w')

# Create a logger object
logger = logging.getLogger(__name__)


class AccountListCreateView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsSalesOrReadOnlyPermission]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = AccountSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = AccountSerializer(data=request.data)

        if serializer.is_valid():
            # Log a debugging message
            logger.debug("Creating account: %s", serializer.data)
            serializer.save(assignee=request.user)
            data = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountSearchView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name', 'email', 'phoneNumber', 'company', 'status', 'assignee']



class AccountRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsAssigneeOrReadOnlyPermission]

    def get_object(self):
        lookup_field = self.kwargs["id"]
        account = get_object_or_404(Account, id=lookup_field)
        # Log a debugging message
        logger.debug("Retrieving account: %s", account)
        return account

    def get_account(self):
        lookup_field = self.kwargs["id"]
        account = get_object_or_404(Account, id=lookup_field)
        # Log a debugging message
        logger.debug("Retrieving account: %s", account)
        return account


class ContractListCreateView(generics.ListCreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsAssigneeOrReadOnlyPermission]
    lookup_field = 'id'

    def get_account(self):
        lookup_field = self.kwargs["id"]
        return get_object_or_404(Account, id=lookup_field)

    def get(self, request, *args, **kwargs):
        lookup_field = self.kwargs["id"]
        queryset = self.get_queryset().filter(account_id=lookup_field)
        serializer = ContractSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        lookup_field = self.kwargs["id"]
        serializer = ContractSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(account_id=lookup_field)
            if serializer.data['status'] == "Signed":
                event_serializer = EventSerializer(data={'status': "Coming", 'contract_id': f'{serializer.data["id"]}'})
                if event_serializer.is_valid():
                    event_serializer.create(
                        validated_data={'status': "Coming", 'contract_id': f'{serializer.data["id"]}'})
                return Response(event_serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error("Invalid serializer data: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractSearchView(generics.ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['account', 'status', 'assignee']


class ContractRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsAssigneeOrReadOnlyPermission]
    queryset = Contract.objects.all()

    def get_account(self):
        lookup_field = self.kwargs["id"]
        return get_object_or_404(Account, id=lookup_field)

    def get_object(self):
        lookup_field = self.kwargs["id"]
        lookup_field2 = self.kwargs["contract_id"]

        try:
            return Contract.objects.get(account_id=lookup_field, id=lookup_field2)
        except Contract.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        snippet = self.get_object()
        serializer = ContractSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if serializer.data['status'] == "Signed":
                event_serializer = EventSerializer(data={'status': "Coming", 'contract_id': f'{serializer.data["id"]}'})
                if event_serializer.is_valid():
                    if Event.objects.all().filter(contract_id=serializer.data['id']).exists():
                        return Response(data="Vous avez modifié un contrat déjà signé ou"
                                             " un évenement lié à ce contrat existe déjà",
                                        status=status.HTTP_400_BAD_REQUEST)
                    event_serializer.create(validated_data={'status': "Coming", 'contract_id': f'{serializer.data["id"]}'})
                return Response(event_serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventSearchView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'contract': ['exact'], 'status': ['exact'], 'assignee': ['exact', 'isnull']}


class EventCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsAssigneeOrReadOnlyPermission]

    def get_account(self):
        lookup_field = self.kwargs["id"]
        return get_object_or_404(Account, id=lookup_field)

    def get_object(self):
        lookup_field = self.kwargs["contract_id"]
        return get_object_or_404(Contract, id=lookup_field)

    def get(self, request, *args, **kwargs):
        lookup_field = self.kwargs["contract_id"]
        queryset = self.get_queryset().filter(contract_id=lookup_field)
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        lookup_field = self.kwargs["contract_id"]
        serializer = EventSerializer(data=request.data)
        if self.get_queryset().filter(contract_id=lookup_field).exists():
            return Response(data="Un évenement lié à ce contrat existe déjà", status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save(contract_id=lookup_field)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsAssigneeOrReadOnlyPermission]

    def get_account(self):
        lookup_field = self.kwargs["id"]
        return get_object_or_404(Account, id=lookup_field)

    def get_object(self):
        lookup_field = self.kwargs["contract_id"]
        return get_object_or_404(Event, contract_id=lookup_field)