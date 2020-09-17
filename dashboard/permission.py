from rest_framework import permissions
from accounts.models import Course


class EditDocumentPermission(permissions.IsAuthenticated):
    """
    Global permission check for blacklisted IPs.
    """

    def has_permission(self, request, view):
        course = Course.objects.get(code=view.kwargs['code'])
        try:
            if course.teacher != request.user and not request.user.is_admin():
                return False
        except:
            return False
        return True
