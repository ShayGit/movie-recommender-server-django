from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from ratings.serializers import RatingSerializer


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name="" if 'first_name' not in validated_data else validated_data['first_name'],
            last_name="" if 'last_name' not in validated_data else validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserRatingSerializer(serializers.ModelSerializer):
    my_ratings = RatingSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('my_ratings',)

    def to_representation(self, user):
        data = super().to_representation(user)
        data['my_movies'] = [rating['movie'] for rating in data['my_ratings']]
        return data
