from .serializers import UserSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Custom response payload handler.
    This function controls the custom payload after login or token refresh. This data is returned through the web API.
    """

    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }