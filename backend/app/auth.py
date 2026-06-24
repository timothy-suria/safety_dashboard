import bcrypt
import secrets
import requests
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "change-this-secret")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24

# Employee auth gateway: checks password + active account
EMPLOYEE_AUTH_URL = os.getenv(
    "EMPLOYEE_AUTH_URL", "http://10.1.20.207:3000/api/auth-employee"
)
EMPLOYEE_AUTH_TIMEOUT = float(os.getenv("EMPLOYEE_AUTH_TIMEOUT", "10"))


def _truncate_password(password: str) -> bytes:
    # bcrypt caps at 72 bytes
    return password.encode("utf-8")[:72]


def hash_password(password: str) -> str:
    pw_bytes = _truncate_password(password)
    return bcrypt.hashpw(pw_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    pw_bytes = _truncate_password(plain)
    return bcrypt.checkpw(pw_bytes, hashed.encode("utf-8"))


def unusable_password_hash() -> str:
    # random hash that never matches; fills the NOT NULL column for gateway users
    return hash_password(secrets.token_urlsafe(32))


class EmployeeAuthResult:
    def __init__(self, ok: bool, message: str, reachable: bool = True):
        self.ok = ok
        self.message = message
        self.reachable = reachable


def verify_employee(identifier: str, password: str) -> EmployeeAuthResult:
    # passes only when password is correct and account is active
    try:
        resp = requests.post(
            EMPLOYEE_AUTH_URL,
            json={"identifier": identifier, "password": password},
            timeout=EMPLOYEE_AUTH_TIMEOUT,
        )
    except requests.RequestException:
        return EmployeeAuthResult(
            False,
            "Layanan autentikasi tidak tersedia. Silakan coba lagi nanti.",
            reachable=False,
        )

    try:
        data = resp.json()
    except ValueError:
        data = {}

    if resp.status_code == 200 and (data.get("status") or "").lower() == "success":
        return EmployeeAuthResult(True, data.get("message") or "Autentikasi berhasil.")

    # pass through the gateway's reason
    return EmployeeAuthResult(
        False, data.get("message") or "Username/Password salah."
    )


def create_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    return jwt.encode({"sub": email, "exp": expire}, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
