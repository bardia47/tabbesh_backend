from accounts.models import *
from rest_framework import serializers


class TeacherSerializer(serializers.ModelSerializer):
    grade_choice = serializers.SerializerMethodField('get_choices')

    class Meta:
        model = User
        fields = ('id', 'avatar', 'get_full_name', 'grade_choice')

    def get_choices(self, instance):
        all_grades = instance.grades.all()
        grades = set()
        for grade in all_grades:
            grades.add(grade.get_grade_choice_display())
        return grades


class CourseSerializer(serializers.ModelSerializer):
    teacher_full_name = serializers.ReadOnlyField(source='teacher.get_full_name')
    course_title = serializers.ReadOnlyField(source='title')
    grade_id = serializers.ReadOnlyField(source='grade.id')

    class Meta:
        model = Course
        fields = ('id', 'image', 'teacher_full_name', 'course_title', 'grade_id')


class CourseDiscountedSerializer(serializers.ModelSerializer):
    teacher_full_name = serializers.ReadOnlyField(source='teacher.get_full_name')
    course_title = serializers.ReadOnlyField(source='title')
    grade_id = serializers.ReadOnlyField(source='grade.id')
    percent = serializers.SerializerMethodField('get_discount_percent')
    discount_name = serializers.SerializerMethodField('get_discount_name')

    class Meta:
        model = Course
        fields = ('id', 'image', 'teacher_full_name', 'course_title', 'grade_id', 'percent', 'discount_name')

    def get_discount_name(self, obj):
        now = datetime.datetime.now()
        query = Q(start_date__lte=now)
        query &= Q(code__isnull=True)
        query &= (Q(end_date__gte=now) | Q(end_date=None))
        query &= (Q(courses__id=obj.id) | Q(courses=None))
        discount = Discount.objects.filter(query)
        if discount.exists():
            return discount.first().title
        return None

    def get_discount_percent(self, obj):
        now = datetime.datetime.now()
        query = Q(start_date__lte=now)
        query &= Q(code__isnull=True)
        query &= (Q(end_date__gte=now) | Q(end_date=None))
        query &= (Q(courses__id=obj.id) | Q(courses=None))
        discount = Discount.objects.filter(query)
        if discount.exists():
            return discount.first().percent
        return None

    # def percent_method(self, instance):
    #     discounts = instance.discount_set
    #     discount = discounts.filter(code=None).first()
    #     return discount.percent


class CourseSerializerTitle(serializers.Serializer):
    title = serializers.CharField(max_length=50)


class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ('description',)
