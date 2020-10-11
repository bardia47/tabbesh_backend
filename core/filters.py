from django_filters import rest_framework
import json
import coreapi

class ListFilter(rest_framework.BaseInFilter):
    def filter_queryset(self, request, queryset, view):
        list = request.GET[view.SEARCH_PARAM]
        if list not in (None, ''):
            # if list.endswith(','):
            #     list = list.rsplit(',', 1)[0]
            # integers = [int(v) for v in list.split(',')]
            return queryset.filter(**{'%s__%s' % (view.search_fields[0], 'in'): json.loads(list)})
        return queryset

    def get_schema_fields(self, view):
        return [coreapi.Field(name='id', location='query', required=True, type='string', example="[1,2,5]")]
