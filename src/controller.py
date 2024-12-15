from typing import List
from fastapi import Depends, HTTPException, status, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .models import TokenResponse, UserInfo, Role, UserNew
from .service import AuthService
from .config import keycloak_admin

# Initialize HTTPBearer security dependency
bearer_scheme = HTTPBearer()


class AuthController:
    """
    Controller for handling authentication logic.
    """

    @staticmethod
    def read_root():
        """
        Root endpoint providing basic information and documentation link.

        Returns:
            dict: A welcome message and link to the documentation.
        """
        return {
            "message": (
                "Welcome to the Keycloak authentication system. "
                "Use the /login endpoint to authenticate and /protected to access the protected resource."
            ),
            "documentation": "/docs",
        }

    @staticmethod
    def login(
            username: str = Form(...),
            password: str = Form(...)
            ) -> TokenResponse:
        """
        Authenticate user and return access token.

        Args:
            username (str): The username of the user attempting to log in.
            password (str): The password of the user.

        Raises:
            HTTPException: If the authentication fails (wrong credentials).

        Returns:
            TokenResponse: Contains the access token upon successful authentication.
        """
        # Authenticate the user using the AuthService
        access_token = AuthService.authenticate_user(username, password)

        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        return TokenResponse(access_token=access_token)

    @staticmethod
    def protected_endpoint(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    ) -> UserInfo:
        """
        Access a protected resource that requires valid token authentication.

        Args:
            credentials (HTTPAuthorizationCredentials): Bearer token provided via HTTP Authorization header.

        Raises:
            HTTPException: If the token is invalid or not provided.

        Returns:
            UserInfo: Information about the authenticated user.
        """
        # Extract the bearer token from the provided credentials
        token = credentials.credentials

        # Verify the token and get user information
        user_info = AuthService.verify_token(token)

        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_info

    @staticmethod
    def role_checker(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    ) -> List[Role]:
        token = credentials.credentials
        data = AuthService.decode_token(token)

        if not data:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="fail to get roles",
                    )
        roles = data.get("realm_access", {}).get("roles", [])

        return roles


def create_new_user(new_user: UserNew) -> str:
    user_id = keycloak_admin.create_user({
        "email": f'{new_user.email}',
        "username": f'{new_user.username}',
        "enabled": f'{new_user.enabled}',
        "firstName": f'{new_user.first_name}',
        "lastName": f'{new_user.last_name}'
        })
    return user_id
