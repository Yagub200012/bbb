import datetime
from symtable import Class

from rest_framework import serializers
from ..models import Post, Comment, SubSector, Sector, Image, Reaction
from ..tasks import upload_image
from notification.models import Notification
from authorization.models import User, AuthorUser
from authorization.api.serializers import UserSerializer, SimpleUserSerializer
from authorization.functions import access
from django.utils import timezone


class RecursiveField(serializers.BaseSerializer):
    def to_representation(self, value):
        serializer = self.parent.__class__(value, context=self.context)
        return serializer.data





class SectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sector
        fields = [
            'id',
            'title',
        ]


class SubSectorSerializer(serializers.ModelSerializer):
    sector = SectorSerializer(read_only=True)

    class Meta:
        model = SubSector
        fields = [
            'id',
            'title',
            'sector'
        ]

    def validate_title(self, value):
        if len(str(value)) > 50:
            raise serializers.ValidationError('Title must be no more than 50 characters')
        return value

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['post','image_link']

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = [
            'type',
        ]

class SimpleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'text'
        ]


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    user = UserSerializer(read_only=True)
    replied_to = SimpleUserSerializer(required=False, read_only=True)
    reaction = serializers.SerializerMethodField(read_only=True, required=False)
    comment_inst = serializers.SerializerMethodField(required=False)


    # post = serializers.IntegerField(required=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
            'created_at',
            'likes',
            'dislikes',
            'user',
            'comment',
            'replied_to',
            'post',
            'reaction',
            'comment_inst',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'likes',
            'dislikes',
            'user',
            'reaction',
            'comment_inst',
            'replied_to',
        ]

    def get_comment_inst(self, obj):
        if obj.comment:
            return SimpleCommentSerializer(obj.comment).data
        return None

    # def get_replied_to_inst(self, obj):
    #     if obj.replied_to:
    #         return SimpleUserSerializer(obj.replied_to).data
    #     return None

    def get_reaction(self,obj):
        access_token = self.context['request'].COOKIES.get('accessToken', None)
        user = None
        if access_token:
            user = access(access_token)
        return ReactionSerializer(
            obj.reaction_set.filter(user= user), many=True
        ).data

    def validate_text(self, value):
        if len(str(value)) > 5000:
            raise serializers.ValidationError('Text must be no more than 5000 characters')
        return value


    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        if validated_data['comment']:
            validated_data['replied_to'] = validated_data['comment'].user
        comment = Comment.objects.create(**validated_data)
        comment.save()
        post = Post.objects.filter(id = validated_data['post'].pk).first()
        post.comments += 1
        post.save()
        if comment.replied_to:
            if comment.replied_to != comment.user:
                Notification.objects.create(
                    user = comment.replied_to,
                    description=f'{comment.user} ответил вам: {comment.text[:70]}',
                    # link=f'/post/{post.id}',
                    post= post,
                    comment = comment,
                    event_date=timezone.now(),
                    type='reply'
                )
        else:
            if comment.user != post.user:
                Notification.objects.create(
                    user=post.user,
                    description=f'{comment.user} оставил комментарий под вашим постом: {comment.text[:70]}',
                    # link=f'/post/{post.id}',
                    post= post,
                    comment = comment,
                    event_date=timezone.now(),
                    type='comment'
                )
        return comment

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     try:
    #         user = self.context['request'].user
    #         is_liked_by_user = Like.objects.filter(user=user, comment=instance)
    #         if is_liked_by_user:
    #             representation['is_liked_by_user'] = True
    #             return representation
    #     except:
    #         pass
    #     representation['is_liked_by_user'] = False
    #     return representation


class PostSerializer(serializers.ModelSerializer):
    reaction = serializers.SerializerMethodField(read_only=True)
    images = ImageSerializer(read_only=True, many=True)
    title = serializers.CharField(required=True)
    content = serializers.CharField(required=False)
    # subsector = serializers.PrimaryKeyRelatedField(queryset=SubSector.objects.all(), required=True)
    anonymously = serializers.BooleanField(required=True)
    user = UserSerializer(read_only=True)
    # subsector = SubSectorSerializer(read_only=True)
    file1 = serializers.FileField(write_only=True,required=False)
    file2 = serializers.FileField(write_only=True,required=False)
    file3 = serializers.FileField(write_only=True,required=False)
    file4 = serializers.FileField(write_only=True,required=False)
    file5 = serializers.FileField(write_only=True,required=False)
    file6 = serializers.FileField(write_only=True,required=False)

    class Meta:
        model = Post
        fields = [
            'comments',
            'id',
            'title',
            'content',
            'created_at',
            'likes',
            'dislikes',
            'subsector',
            'user',
            'anonymously',
            'images',
            'reaction',
            'file1',
            'file2',
            'file3',
            'file4',
            'file5',
            'file6',
        ]
        read_only_fields = [
            'comments',
            'id',
            'created_at',
            'reaction',
            'likes',
            'dislikes',
            'user',
        ]

    def get_reaction(self,obj):
        access_token = self.context['request'].COOKIES.get('accessToken', None)
        user = None
        if access_token:
            user = access(access_token)
        return ReactionSerializer(
            obj.reaction_set.filter(user= user), many=True
        ).data

    def create(self, validated_data):
        # validated_data['user'] = self.context['request'].user
        post = Post.objects.create(
            user = self.context['request'].user,
            title = validated_data['title'],
            content = validated_data['content'],
            subsector = validated_data['subsector'],
            anonymously = validated_data['anonymously'],
        )
        for i in range(1, 7):
            if f"file{i}" in validated_data:
                image = validated_data.pop(f"file{i}")
                upload_image.delay(image.read(), post.id)
        return post

    def validate_title(self, value):
        if len(str(value)) > 100:
            raise serializers.ValidationError('Title must be no more than 100 characters')
        return value

    def validate_content(self, value):
        if len(str(value)) > 5000:
            raise serializers.ValidationError('Post text must be no more than 5000 characters')
        return value


class SubSectorPostSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True,
                           # source='posts'
                           )

    class Meta:
        model = SubSector
        fields = [
            'id',
            'title',
            'posts',
        ]

    def validate_title(self, value):
        if len(str(value)) > 50:
            raise serializers.ValidationError('Title must be no more than 50 characters')
        return value

