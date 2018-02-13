from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from discussion.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password')

class DiscussionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Discussion
		exclude = ('created_date', 'modified_date')

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		exclude = ('created_date', 'modified_date')