from django.http import JsonResponse
from django.views import View
from loguru import logger

class TestLoggingView(View):
    def get(self, request):
        logger.debug("This is a debug Message")
        logger.info("This is a info Message")
        logger.warning("This is a warning Message")
        logger.error("This is a error Message")
        logger.critical("This is a critical Message")
        return JsonResponse({"message": "We are testing loguru"})