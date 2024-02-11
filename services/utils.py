from abc import ABC

import httpx


class BaseAPIHttpxClass(ABC):
    def __init__(self):
        self.client = self._create_httpx_client()

    def _create_httpx_client(self) -> httpx.Client:
        """
        Create Logging for request/response for API # TODO add logger
        """

        def log_request(request):
            print(f"Request : {request.method} {request.url} - Waiting for response")

        def log_response(response):
            request = response.request
            print(
                f"Response : {request.method} {request.url} - Status {response.status_code}"
            )

        if self.async_client:
            client = httpx.AsyncClient
        else:
            client = httpx.Client

        return client(
            event_hooks={"request": [log_request], "response": [log_response]}
        )
