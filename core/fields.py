from rest_framework import serializers
from rest_framework.reverse import reverse


class SearchHyperlinkField(serializers.HyperlinkedIdentityField):
    # We define these as class attributes, so we don't need to pass them as arguments.
    def __init__(self, view_name=None, search_field=None, param_name=None, **kwargs):
        self.search_field = search_field
        self.param_name = param_name
        super().__init__(view_name, **kwargs)

    def get_url(self, obj, view_name, request, format):
        return '{0}?{1}={2}'.format(reverse(view_name, request=request, format=format),self.param_name,getattr(obj, self.search_field))
