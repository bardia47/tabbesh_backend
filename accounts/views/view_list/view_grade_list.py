from accounts.models import Grade
from rest_framework import generics
from accounts.serializers.serializer_list.serializer_list_grade import GradeListSerializer

class GradeListView(generics.ListAPIView):
    serializer_class = GradeListSerializer
    queryset = Grade.objects.all()
