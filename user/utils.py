import base64
import random
import string
import hashlib
from typing import Union, Any
from datetime import datetime, timedelta
from urllib.parse import urljoin

from config import settings

import httpx
from jose import jwt


def sha256_hash(string: str) -> str:
    """
    Hash string in sha256
    """
    return hashlib.sha256(string.encode()).hexdigest()


def compare_password(password: str, hashed_password: str) -> bool:
    """
    Compare password
    """
    return sha256_hash(password) == hashed_password


def create_access_token(object: Union[str, Any], expires_delta: int = None) -> str:
    """
    Create JWT token for user
    """
    if expires_delta:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    to_encode = {"exp": expires_delta, "sub": str(object)}
    jwt_encoded = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return jwt_encoded


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    """
    Create JWT refresh token
    """
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=int(settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_KEY, settings.ALGORITHM)
    return encoded_jwt


def generate_random_string(length: int = 16) -> str:
    symbols = string.ascii_letters + string.digits
    return "".join(random.choice(symbols) for _ in range(length))


def send_email(email: str, message: str = "", subject: Union[str, None] = None) -> None:
    if settings.SEND_EMAIL:
        SendPulseEmailService(message=message, to=email, subject=subject).execute()


class SendPulseEmailService:
    """
    Class to send email
    """

    def __init__(
        self, message: str, subject: Union[str, None], to: list[dict], html: str = ""
    ) -> None:
        self.message = message
        self.html = base64.b64encode(html.encode() or f"<p>{message}</p>".encode())
        self.url = "https://api.sendpulse.com/"
        self.subject = subject or "Restore password"
        self.headers = {
            "Authorization": f"Bearer {settings.SENDPULSE_API_ID}:{settings.SENDPULSE_API_SECRET}"
        }
        self.email_from = {"name": "Time Blend", "email": "TimeBlend@email.com"}
        self.to = to
        self.client = self._create_httpx_client()

    def execute(self) -> None:
        """
        Send message to
        """
        self._auth_in_service()
        data = self._prepare__email_request()
        url = urljoin(self.url, "smtp/emails")
        response = self.client.post(url=url, json=data)
        if response.is_error:
            print("error in response")
        print(response.json())
        self.client.close()

    def _prepare__email_request(self) -> dict:
        return {
            "email": {
                "html": self.html.decode(),
                "text": self.message,
                "subject": self.subject,
                "from": self.email_from,
                "to": self.to,
            }
        }

    def _auth_in_service(self) -> None:
        url = urljoin(self.url, "/oauth/access_token")
        data = {
            "grant_type": "client_credentials",
            "client_id": settings.SENDPULSE_API_ID,
            "client_secret": settings.SENDPULSE_API_SECRET,
        }
        response = self.client.post(url=url, json=data)
        if response.is_success:
            data = {"Authorization": f'Bearer {response.json().get("access_token")}'}
            self.client.headers.update(data)

    @staticmethod
    def _create_httpx_client() -> httpx.Client:
        """
        Create client with logging
        """

        def log_request(request):
            print(f"Request : {request.method} {request.url} - Waiting for response")

        def log_response(response):
            request = response.request
            print(
                f"Response : {request.method} {request.url} - Status {response.status_code}"
            )

        return httpx.Client(
            event_hooks={"request": [log_request], "response": [log_response]}
        )
