from rest_framework import serializers
from .models import Contract


class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = ['id', 'status', 'amount', 'account', 'created_time', 'edited_time', 'assignee', 'signature_time']
        read_only_fields = ['id', 'created_time', 'edited_time']