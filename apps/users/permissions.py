from rest_framework.permissions import BasePermission

from rest_framework_jwt.utils import jwt_decode_handler


def get_auth0_user_id_from_request(request):
    token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
    payload = jwt_decode_handler(token)
    return payload.get('user_id')


class IsAuthorUser(BasePermission):
    """
    Allows access only to author users.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_author)


class IsOwnBook(IsAuthorUser):
    def has_object_permission(self, request, view, obj):
        auth0_user_id = get_auth0_user_id_from_request(request)
        return bool(auth0_user_id == obj.author.id)


class IsLibrarianUser(BasePermission):
    """
    Allows access only to librarian  users.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_librarian)


class IsNormalUser(BasePermission):
    """
    Allows access     users.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)
