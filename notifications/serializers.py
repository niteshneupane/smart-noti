from rest_framework.serializers import ModelSerializer, Serializer, ListField, IntegerField, ValidationError, Field, ChoiceField, JSONField
from .models import Notification, NotificationPreference, EVENT_TYPES

class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class MultiSelectSerializerField(Field):
    def to_representation(self, value):
        if not value:
            return []
        return value

    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise ValidationError('Expected a list of strings.')
        return ','.join(data)

class NotificationPreferenceSerializer(ModelSerializer):
    comment = MultiSelectSerializerField()
    unauthorized_login = MultiSelectSerializerField()
    summary = MultiSelectSerializerField()

    class Meta:
        model = NotificationPreference
        exclude = ['user']

class ReadNotificationSerializer(Serializer):
    id = IntegerField()

class TriggerEventSerializer(Serializer):
    event_type = ChoiceField(choices=[e[0] for e in EVENT_TYPES])
    payload = JSONField()


