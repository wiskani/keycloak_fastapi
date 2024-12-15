from fastapi import FastAPI, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .models import TokenResponse, UserInfo, UserNew
from .controller import AuthController,  create_new_user

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
@app.get("/roles")
async def roles_endpoint(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        ):
    return AuthController.role_checker(credentials)


@app.get("/states")
async def states_list(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        ):
    """
    Endpoint to list states, accessible only to users with specific roles.

    Args:
        credentials (HTTPAuthorizationCredentials): Bearer token provided via HTTP Authorization header.

    Returns:
        dict: Message indicating success or failure based on role verification.
    """
    # Obtener roles del token
    roles = AuthController.role_checker(credentials)

    required_roles = {"AgentRole"}
    if not required_roles.intersection(roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )

    return {
        "message": "The users can view the list of states",
    }


@app.post("/user")
async def create_user_api(
        new_user: UserNew,
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        ) -> str:
    return create_new_user(new_user)
