from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user object
    """

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

        def create(self, validate_data):
            """
            Create a new user
            """
            return get_user_model().objects.create_user(**validate_data)


class AuthTokenSerializer(serializers.Serializer):

    """
    Serializer for user auth token
    """
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """
        Validate and authenticate the user
        """
        email = attrs.get('email')
        password = attrs.get('email')

        user = authenticate(
            request=self.comtext.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate')
            raise serializers.ValidatationError(msg, code='autenticate')
        attrs['user'] = user
        return attrs
