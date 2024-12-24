# utils.py
from rest_framework.views import exception_handler
from rest_framework.response import Response

def CustomExceptionHandler(exc, context):
    """
    Custom exception handler that formats errors in the desired structure.
    """
    # Get the default error response from DRF
    response = exception_handler(exc, context)

    # If there's no response, return an empty error list
    if response is None:
        return Response({"errors": [str(exc)]}, status=500)

    # Format the errors consistently
    if response.data:
        return Response({"errors": response.data}, status=response.status_code)

    return response
