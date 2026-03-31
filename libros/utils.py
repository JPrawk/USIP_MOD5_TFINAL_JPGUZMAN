from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def permission_required(perm):
    """
    Decorador personalizado de permisos para vistas de libros.
    :param perm: lista de permisos requeridos
    :return: True si tiene permisos, PermissionDenied si no
    """
    def check_perms(user):
        if user.has_perms(perm) or user.is_superuser:
            return True
        raise PermissionDenied
    return user_passes_test(check_perms)