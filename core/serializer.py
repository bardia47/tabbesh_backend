from rest_framework import serializers


class SuccessSerializer(serializers.Serializer):
    detail = serializers.CharField()

    class Meta:
        fields = ('detail')

    def __init__(self, message, **kwargs):
        super().__init__(data={"detail": message}, **kwargs)
