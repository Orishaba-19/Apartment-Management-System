import logging
import traceback
import uuid
from django.shortcuts import render

logger = logging.getLogger(__name__)


class ExceptionLoggingMiddleware:
    """Middleware that logs unhandled exceptions to a file and shows a friendly error page.

    It generates a unique error id for each exception which is displayed to the user
    and logged together with the traceback so you can correlate reports.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as exc:
            error_id = uuid.uuid4().hex
            tb = traceback.format_exc()
            logger.exception(
                "Error ID %s - Unhandled exception:\n%s", error_id, tb)

            # Render a friendly page with the error id
            try:
                return render(request, '500_custom.html', {'error_id': error_id}, status=500)
            except Exception:
                # If template render fails, still return a minimal response
                from django.http import HttpResponse
                return HttpResponse(f"An internal error occurred. Reference: {error_id}", status=500)
