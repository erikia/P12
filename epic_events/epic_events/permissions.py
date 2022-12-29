from rest_framework import permissions


class IsAssigneeOrReadOnlyPermission(permissions.BasePermission):
    message = "Vous n'êtes pas assigné à cet élément"

    def has_permission(self, request, view):
        if request.user.role == "Admin":
            return True
        assignee = view.get_account().assignee
        if assignee == request.user.id:
            return True
        if view.get_object().assignee == request.user:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True


class IsSalesOrReadOnlyPermission(permissions.BasePermission):
    message = "Vous ne faites pas partie de l'équipe de vente"

    def has_permission(self, request, view):
        if request.user.role == "Sales" or request.user.role == "Admin":
            return True
        elif request.method in permissions.SAFE_METHODS:
            return True
