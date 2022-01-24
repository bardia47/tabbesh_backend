#
# def document_directory_path(instance, filename):
#     return 'documents/{0}/{1}'.format(instance.course.code, filename)
#
# # Documents_model
# class Document(models.Model):
#     course = models.ForeignKey(
#         'Course', on_delete=models.DO_NOTHING, verbose_name="دوره")
#     upload_document = models.FileField(
#         'فایل', upload_to=document_directory_path, null=True, blank=True)
#     upload_date = models.DateTimeField("تاریخ بارگذاری", auto_now_add=True)
#     title = models.CharField("عنوان", max_length=60)
#     description = models.TextField("توضیحات", null=True, blank=True)
#     sender = models.ForeignKey(
#         'User', on_delete=models.DO_NOTHING, verbose_name="فرد بارگذار")
#
#     class Meta:
#         ordering = ['-upload_date']
#         verbose_name_plural = "فایل ها"
#         verbose_name = "فایل ها"
#
#     def __str__(self):
#         return self.title
#
#     def upload_date_decorated(self):
#         return datetime2jalali(self.upload_date).strftime('%y/%m/%d _ %H:%M:%S')
#
#     upload_date_decorated.short_description = 'تاریخ بارگذاری'
