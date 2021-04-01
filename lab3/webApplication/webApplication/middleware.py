from datetime import datetime
import logging

logger = None


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global logger
        if logger is None:
            logging.basicConfig(
                level=logging.DEBUG,
                format='Middleware Logger: %(levelname)s - %(asctime)s - %(message)s',
                datefmt='%Y-%m-%d %X',
            )
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)

        request.logger = logger
        response = self.get_response(request)
        return response

