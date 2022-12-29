from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'status', 'contract', 'notes', 'assignee', 'attendees', 'date']
        read_only_fields = ['id', 'contract']
