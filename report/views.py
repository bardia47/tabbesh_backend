# for load or dump jsons


# class ClassList(generics.RetrieveAPIView):
#     renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
#     queryset = Course.objects.all()
#     serializer_class = FilesSerializer
#     lookup_field = 'code'
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         students = instance.user_set.all()
#         listSerializer = ClassListSerializer(instance={'students': students, 'course': instance},
#                                              context={'course_id': instance.id})
#         return Response(listSerializer.data)
