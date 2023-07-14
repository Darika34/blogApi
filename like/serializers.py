from rest_framework import serializers
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        post = attrs['post']
        if user.likes.filter(post=post).exists():
            raise serializers.ValidationError(
                '<you already liked this post>-  agressive Ertay mood on!'
            )
        return attrs