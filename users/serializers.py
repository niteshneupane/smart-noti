


from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from django.contrib.auth.models import User
from django.utils.timezone import now
from .models import KnownDevice
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from notifications.utils import dispatch_notification
from notifications.models import NotificationPreference


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        print("Inside validation")
        data = super().validate(attrs)

        user = self.user
        request = self.context.get('request')
        user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')


        known = KnownDevice.objects.filter(user=user, user_agent=user_agent).exists()

        print(f"Known {known}")

        if not known:
            print(f"Not Knownnnnn {known}")

            dispatch_notification(
                user=user,
                title="New Device Login",
                body="We noticed a login from a device we haven't seen before.",
                event_type='unrecog_login'
            )
            KnownDevice.objects.create(
                user=user,
                user_agent=user_agent,
                last_seen=now()
            )

        return data

class RegisterSerializer(ModelSerializer):
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    email = CharField(required=True)
    password = CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = CharField(write_only=True, required=True,style={'input_type': 'password'}, label="Confirm password")

    class Meta:
        model = User
        fields = ('first_name','last_name','email','password','password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError({"password": "Passwords do not match."})
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("A user with that email already exists.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')

        validated_data.pop('password2')
        email = validated_data['email']
        user = User.objects.create_user(username=email, **validated_data)
        
        KnownDevice.objects.create(
            user=user,
            user_agent=user_agent,
            last_seen=now()
        )
        return user
