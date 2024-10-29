from rest_framework import serializers
from .models import Complaint

class ComplaintSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    description = serializers.CharField(required=True)

    class Meta:
        model = Complaint
        fields = ['id', 'description', 'location', 'status', 'created_at', 'due_date', 'image', 'user', 'user_id']

    def create(self, validated_data):
        return Complaint.objects.create(**validated_data)
