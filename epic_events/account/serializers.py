from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'first_name', 'last_name', 'email', 'phoneNumber', 'secondPhoneNumber', 'company',
                  'phoneNumber', 'status', 'created_time', 'edited_time', 'assignee']
        read_only_fields = ['id', 'created_time', 'edited_time']