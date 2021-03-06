from django.contrib.auth.models import User, Group
from .models import Post, Comment
from api_auth.serializers import UserSerializer, SubUserSerializer
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    like = UserSerializer(read_only=True, many=True)
    owner = SubUserSerializer(read_only=True, required=False)

    class Meta:
        model = Comment
        fields = [
                  'post',
                  'content',
                  'date',
                  'id',
                  'parent_comment',
                  'like',
                  'owner',
                  ]


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True, required=False)
    like = UserSerializer(read_only=True, many=True, required=False)
    owner = SubUserSerializer(read_only=True, required=False)

    class Meta:
        model = Post
        fields = [
                  'title',
                  'description',
                  'date',
                  'id',
                  'comments',
                  'picture',
                  'like',
                  'owner',
                  ]
