from rest_framework import serializers
from .models import UserAccount, Invito

class UserAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'first_name', 'last_name', 'data_iscrizione']
        read_only_fields = ['id', 'data_iscrizione']


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invito
        fields = ['uuid', 'email', 'employee_uuid', 'exec_time', 'status', 'error_description']
        read_only_fields = ['uuid', 'exec_time']
