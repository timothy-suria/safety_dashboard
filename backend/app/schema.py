import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import Optional
from sqlalchemy.orm import Session
import random

from app import models, auth
from app.database import get_db
from app.email_service import send_verification_email


def _get_db() -> Session:
    return next(get_db())


def _gen_code() -> str:
    return str(random.randint(100000, 999999))


@strawberry.type
class UserType:
    id: int
    email: str
    verified: bool


@strawberry.type
class AuthPayload:
    success: bool
    message: str
    token: Optional[str] = None
    user: Optional[UserType] = None


@strawberry.type
class Query:
    @strawberry.field
    def me(self, info: strawberry.types.Info) -> Optional[UserType]:
        request = info.context["request"]
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.removeprefix("Bearer ").strip()
        if not token:
            return None
        email = auth.decode_token(token)
        if not email:
            return None
        db = _get_db()
        user = db.query(models.User).filter(models.User.email == email).first()
        db.close()
        if not user:
            return None
        return UserType(id=user.id, email=user.email, verified=user.verified)


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def register(self, email: str, password: str) -> AuthPayload:
        if not email.endswith("@cp.co.id"):
            return AuthPayload(success=False, message="Email must be a @cp.co.id address")
        if len(password) < 6:
            return AuthPayload(success=False, message="Password must be at least 6 characters")

        db = _get_db()
        try:
            existing = db.query(models.User).filter(models.User.email == email).first()
            if existing:
                return AuthPayload(success=False, message="Email already registered")

            code = _gen_code()
            user = models.User(
                email=email,
                hashed_password=auth.hash_password(password),
                verified=False,
                verification_code=code,
            )
            db.add(user)
            db.commit()

            await send_verification_email(email, code)
            return AuthPayload(success=True, message=f"Verification code sent to {email}")
        except Exception as e:
            db.rollback()
            return AuthPayload(success=False, message=f"Registration failed: {str(e)}")
        finally:
            db.close()

    @strawberry.mutation
    def verify_email(self, email: str, code: str) -> AuthPayload:
        db = _get_db()
        try:
            user = db.query(models.User).filter(models.User.email == email).first()
            if not user:
                return AuthPayload(success=False, message="User not found")
            if user.verification_code != code:
                return AuthPayload(success=False, message="Invalid verification code")

            user.verified = True
            user.verification_code = None
            db.commit()

            token = auth.create_token(email)
            return AuthPayload(
                success=True,
                message="Email verified successfully",
                token=token,
                user=UserType(id=user.id, email=user.email, verified=True),
            )
        finally:
            db.close()

    @strawberry.mutation
    def login(self, email: str, password: str) -> AuthPayload:
        if not email.endswith("@cp.co.id"):
            return AuthPayload(success=False, message="Invalid email format")

        db = _get_db()
        try:
            user = db.query(models.User).filter(models.User.email == email).first()
            if not user:
                return AuthPayload(success=False, message="User not found. Please register first")
            if not auth.verify_password(password, user.hashed_password):
                return AuthPayload(success=False, message="Invalid password")
            if not user.verified:
                return AuthPayload(success=False, message="Please verify your email before logging in")

            token = auth.create_token(email)
            return AuthPayload(
                success=True,
                message="Login successful",
                token=token,
                user=UserType(id=user.id, email=user.email, verified=user.verified),
            )
        finally:
            db.close()

    @strawberry.mutation
    async def resend_verification(self, email: str) -> AuthPayload:
        db = _get_db()
        try:
            user = db.query(models.User).filter(models.User.email == email).first()
            if not user:
                return AuthPayload(success=False, message="User not found")
            if user.verified:
                return AuthPayload(success=False, message="Email already verified")

            code = _gen_code()
            user.verification_code = code
            db.commit()

            await send_verification_email(email, code)
            return AuthPayload(success=True, message=f"Verification code resent to {email}")
        except Exception as e:
            db.rollback()
            return AuthPayload(success=False, message=f"Failed to resend: {str(e)}")
        finally:
            db.close()


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_router = GraphQLRouter(schema)
