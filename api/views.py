from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from discussion.models import *
from discussion.serializers import *
from django.db.models import Q
from rest_framework.views import APIView


class register(APIView):
	def post(self, request, format=None):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			psw1 = request.data['password']
			psw2 = request.data['confirm_password']
			if psw1 == psw2:
				obj = serializer.save()
				obj.set_password(request.data['password'])
				obj.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response({'error': 'Both passwords must be same...!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
@api_view(['POST'])
def register(request):
	serializer = UserSerializer(data=request.data)
	if serializer.is_valid():
		psw1 = request.data['password']
		psw2 = request.data['confirm_password']
		if psw1 == psw2:
			obj = serializer.save()
			obj.set_password(request.data['password'])
			obj.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response({'error': 'Both passwords must be same...!'}, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""


class artque_list(APIView):
	def get(self, request, format=None):
		artque = Discussion.objects.filter(title_type__in=['article','question'])
		serializer = DiscussionSerializer(artque, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


"""
@api_view(['GET'])
def artque_list(request):
	artque = Discussion.objects.filter(title_type__in=['article','question'])
	serializer = DiscussionSerializer(artque, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)
"""


class comment_add(APIView):
	authentication_classes = (TokenAuthentication,)

	def post(self, request, format=None):
		if request.user.is_authenticated():
			owner = request.user
			data = request.data
			data['added_by'] = owner.id
			serializer = CommentSerializer(data=data)
			if serializer.is_valid():
				d_id = request.data['discussion']
				comment = Comment.objects.filter(discussion=d_id, added_by=owner.id).exists()
				if comment == True:
					return Response({'error': 'You already commented earlier.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
				else:
					obj = Discussion.objects.get(id=d_id)
					dis_list = Discussion.objects.filter(added_by=owner.id)
					if obj in dis_list:
						return Response({'error': 'You can not comment on your own Discussion.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
					else:
						serializer.save()
						return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({'error': 'You are not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


"""
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
def comment_add(request):
	if request.user.is_authenticated():
		owner = request.user
		data = request.data
		data['added_by'] = owner.id
		serializer = CommentSerializer(data=data)
		if serializer.is_valid():
			d_id = request.data['discussion']
			comment = Comment.objects.filter(discussion=d_id, added_by=owner.id).exists()
			if comment == True:
				return Response({'error': 'You already commented earlier.'}, status=status.HTTP_200_OK)
			else:
				obj = Discussion.objects.get(id=d_id)
				dis_list = Discussion.objects.filter(added_by=owner.id)
				if obj in dis_list:
					return Response({'error': 'You can not comment on your own Discussion.'}, status=status.HTTP_200_OK)
				else:
					serializer.save()
					return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response({'error': 'You are not authenticated'}, status=status.HTTP_200_OK)
"""


class discussion_list(APIView):
	def get(self, request, format=None):
		try:
			title = request.GET['title']
		except:
			title = []
		try:
			text = request.GET['text']
		except:
			text = []
		try:
			title_type = request.GET['title_type']
		except:
			title_type = []

		if title == text == title_type == []:
			discussion = Discussion.objects.all()
		else:
			discussion = Discussion.objects.filter(Q(title__icontains=title) | Q(text__icontains=text) | Q(title_type__icontains=title_type))
			#discussion = Discussion.objects.filter(Q(title__icontains=title) & Q(text__icontains=text) & Q(title_type__icontains=title_type))
		
		serializer = DiscussionSerializer(discussion, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


"""
@api_view(['GET'])
def discussion_list(request):
	title = request.GET['title']
	text = request.GET['text']
	title_type = request.GET['title_type']

	discussion = Discussion.objects.filter(Q(title__icontains=title) | Q(text__icontains=text) | Q(title_type__icontains=title_type))
	serializer = DiscussionSerializer(discussion, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)
"""
