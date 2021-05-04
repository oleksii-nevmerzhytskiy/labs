from rest_framework import serializers
from .models import ContactModel


class ContactSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)

	class Meta:
		model = ContactModel
		depth = 1
		fields = '__all__'

