from rest_framework import serializers
from .models import Event, Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'image']

class EventSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['event_id', 'event_name', 'num_teams', 'event_purpose', 'created_at', 'dummy_field', 'teams']
