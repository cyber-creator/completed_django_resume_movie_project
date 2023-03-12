from rest_framework import permissions
# our permissions


class IsHaveAccountPerm(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.groups.exists():
            group_list = []
            for groups in request.user.groups.all():
                group_list.append(str(groups).lower())

            if 'allowed_edit' in group_list:
                return True
            # elif 'allowed' in group_list and request.method in permissions.SAFE_METHODS:
            #     return True

        elif request.method in permissions.SAFE_METHODS:
            return True

        return False
