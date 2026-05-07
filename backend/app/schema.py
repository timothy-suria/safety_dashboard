import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import Optional
from sqlalchemy.orm import Session

from app import models, auth
from app.database import get_db


def _get_db() -> Session:
    return next(get_db())


@strawberry.type
class UserType:
    id: int
    email: str


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
        return UserType(id=user.id, email=user.email)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def register(self, email: str, password: str) -> AuthPayload:
        if not email.endswith("@cp.co.id"):
            return AuthPayload(success=False, message="Email must be a @cp.co.id address")
        if len(password) < 6:
            return AuthPayload(success=False, message="Password must be at least 6 characters")

        db = _get_db()
        try:
            if db.query(models.User).filter(models.User.email == email).first():
                return AuthPayload(success=False, message="Email already registered")

            user = models.User(
                email=email,
                hashed_password=auth.hash_password(password),
            )
            db.add(user)
            db.commit()
            db.refresh(user)

            token = auth.create_token(email)
            return AuthPayload(
                success=True,
                message="Registration successful",
                token=token,
                user=UserType(id=user.id, email=user.email),
            )
        except Exception as e:
            db.rollback()
            return AuthPayload(success=False, message=f"Registration failed: {str(e)}")
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

            token = auth.create_token(email)
            return AuthPayload(
                success=True,
                message="Login successful",
                token=token,
                user=UserType(id=user.id, email=user.email),
            )
        finally:
            db.close()


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_router = GraphQLRouter(schema)
