from rest_framework import permissions


class IsUserDocumentalista(permissions.BasePermission):
    """
    Permite acceso de lectura a todos.
    Solo usuarios del grupo Documentalista pueden modificar.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user and
            request.user.groups.filter(name='Documentalista').exists()
        )


class IsUserAdmin(permissions.BasePermission):
    """
    Solo usuarios del grupo Admin tienen acceso completo.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.groups.filter(name='Admin').exists()
        )