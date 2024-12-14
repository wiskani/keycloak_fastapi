from fastapi import FastAPI, Depends, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .models import TokenResponse, UserInfo
from .controller import AuthController

app = FastAPI()

# Initialize the HTTPBearer scheme for autentication
bearer_scheme = HTTPBearer()


# Root endpoint
@app.get("/")
async def read_root():
    """
    Root endpoint that provides a welcome message and documentation link.
    """
    return AuthController.read_root()


# Define the login endpoint
@app.post("/login", response_model=TokenResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    """
    login endpoint to authenticate the user and return an access toke.

    Args:
        username (str): The username of the user attempting to log in.
        password (str): The password of the user.

    Returns:
        TokenResponse: Contains the access token upon successful authentication.
    """
    return AuthController.login(username, password)


# Define the protected endpoint
@app.get("/protected", response_model=UserInfo)
async def protected_endpoint(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        ):
    """
    Protected endpoint that requires a valid token for access.

    Args:
        credentials (HTTPAuthorizationCredentials):
            Bearer token provided via HTTP Authorization header.

    Returns:
        UserInfo: Information about the authenticated user.
    """

    return AuthController.protected_endpoint(credentials)


# Define the protected endpoint return permision
@app.get("/permision", response_model=UserInfo)
async def permision_endpoint(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        ):
    return AuthController.permissions_endpoint(credentials)


@app.get("/states")
async def states_list(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        ):
    return {
            "message": (
                "The users can view list states"
            ),
        }
