from django_filters import rest_framework


class ListFilter(rest_framework.BaseInFilter):
    def filter_queryset(self, request, queryset, view):
        list = request.GET[view.SEARCH_PARAM]
        if list not in (None, ''):
            if list.endswith(','):
                list = list.rsplit(',', 1)[0]
            integers = [int(v) for v in list.split(',')]
            return queryset.filter(**{'%s__%s' % (view.search_fields[0], 'in'): integers})
        return queryset
