from rest_framework import serializers


# TODO Сериалайзеры. Предлагаем Вам такую структуру, однако вы вправе использовать свою
class CommentSerializer(serializers.ModelSerializer):
    # TODO сериалайзер для модели
    comment_ad = serializers.CharField(read_only=True)
    comment_user = serializers.CharField(read_only=True)
    comment_text = serializers.CharField()
    comment_create = serializers.DateTimeField(read_only=True)


class AdSerializer(serializers.ModelSerializer):
    # TODO сериалайзер для модели
    author = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=128)
    price = serializers.IntegerField()
    image = serializers.ImageField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class AdDetailSerializer(serializers.ModelSerializer):
    # TODO сериалайзер для модели
    pass
