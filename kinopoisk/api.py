from config import settings

import httpx


class KinoPoiskAPI:
    """
    Class to get data from kinopoisk
    """

    ulr = "https://api.kinopoisk.dev/"
    token = settings.KINOPOISK_TOKEN

    def __init__(self):
        self.client = httpx.Client()
        self.__prepare_header()

    def __prepare_header(self):
        """
        Prepare header for authorize
        """
        self.client.headers.update({"X-API-KEY": self.token})
