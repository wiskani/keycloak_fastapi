from fastapi import HTTPException, status
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakGetError
from .config import keycloak_openid
from .models import UserInfo


class AuthService:
    @staticmethod
    def authenticate_user(username: str, password: str) -> str:
        """
        Authenticate the user using Keycloak and return an access token.
        """
        try:
            token = keycloak_openid.token(username, password)
            return token["access_token"]
        except KeycloakAuthenticationError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

    @staticmethod
    def verify_token(token: str) -> UserInfo:
        """
        Verify the given token and return user information.
        """
        try:
            user_info = keycloak_openid.userinfo(token)
            print(user_info)
            if not user_info:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
            return UserInfo(
                preferred_username=user_info["preferred_username"],
                email=user_info.get("email"),
                full_name=user_info.get("name"),
            )
        except KeycloakAuthenticationError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'Could not validate credentials: {e}',
            )

    @staticmethod
    def decode_token(token: str):
        """
        Get permissions for a user
        """
        try:
            token_decode = keycloak_openid.decode_token(token)
            print(token_decode)
            if not token_decode:
                raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="there are a proble with role information in token"
                        )
            return token_decode
        except KeycloakGetError as e:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Could not find token information: {e}',
                    )
