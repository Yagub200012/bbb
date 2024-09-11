from django.template.defaulttags import comment
from rest_framework import serializers
from ..models import Post, Like, Comment, SubSector, Sector
from authorization.models import User


class LikeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False)
    comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False)

    class Meta:
        fields = [
            'id'
            'post',
            'user',
            'comment',
        ]
        read_only_fields = ['id']

    def validate(self, data):
        post = data.get('post')
        comment = data.get('comment')
        if (post and comment) or ((not post) and (not comment)):
            raise serializers.ValidationError("Requires either the comment ID or the post ID only")
        return data


    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        comment.user = self.context['request'].user
        comment.save()
        return comment


class RecursiveField(serializers.BaseSerializer):
    def to_representation(self, value):
        serializer = self.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    user = serializers.IntegerField(required=True)
    parent = serializers.IntegerField(required=True)
    sub_comments = RecursiveField(many=True, required=False)

    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
            'created_at',
            'likes',
            'user',
            'parent',
        ]
        read_only_fiealds = [
            'id',
            'created_at',
            'likes',
            'sub_comments',
        ]

    def validate_text(self, value):
        if len(str(value)) > 5000:
            raise serializers.ValidationError('Text must be no more than 5000 characters')
        return value

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        comment.user = self.context['request'].user
        comment.save()
        return comment

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            user = self.context['request'].user
            is_liked_by_user = Like.objects.filter(user=user, comment=instance)
            if is_liked_by_user:
                representation['is_liked_by_user'] = True
                return representation
        except:
            pass
        representation['is_liked_by_user'] = False
        return representation


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    content = serializers.CharField(required=True)
    subsector = serializers.PrimaryKeyRelatedField(queryset=SubSector.objects.all(), required=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'created_at',
            'likes',
            'subsector',
            'user',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'likes',
            'user',
        ]

    def create(self, validated_data):
        # Здесь subsector уже будет объектом SubSector, так как это обработано сериализатором
        post = Post.objects.create(**validated_data)
        post.user = self.context['request'].user
        post.save()
        return post

    def validate_title(self, value):
        if len(str(value)) > 100:
            raise serializers.ValidationError('Title must be no more than 100 characters')
        return value

    def validate_content(self, value):
        if len(str(value)) > 5000:
            raise serializers.ValidationError('Post text must be no more than 5000 characters')
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            user = self.context['request'].user
            is_liked_by_user = Like.objects.filter(user=user, post=instance).exists()
            representation['is_liked_by_user'] = is_liked_by_user
        except:
            representation['is_liked_by_user'] = False
        return representation


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


class SubSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSector
        fields = [
            'id',
            'title',
        ]

    def validate_title(self, value):
        if len(str(value)) > 50:
            raise serializers.ValidationError('Title must be no more than 50 characters')
        return value


class SectorSerializer(serializers.ModelSerializer):
    subsector = SubSectorSerializer(many=True, read_only=True, source='subsectors')

    class Meta:
        model = Sector
        fields = [
            'id',
            'title',
            'subsector',
        ]

    def validate_title(self, value):
        if len(str(value)) > 50:
            raise serializers.ValidationError('Title must be longer than 50 characters')
        return value
