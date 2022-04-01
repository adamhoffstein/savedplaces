from fastapi import HTTPException


EMAIL_USERNAME_ALREADY_REGISTERED = HTTPException(
    status_code=400, detail="Email and username already registered."
)

USER_NOT_IN_WHITELIST = HTTPException(
    status_code=400, detail="You're not supposed to be here."
)

EMAIL_ALREADY_REGISTERED = HTTPException(
    status_code=400, detail="Email already registered."
)

USERNAME_ALREADY_REGISTERED = HTTPException(
    status_code=400, detail="Username already registered."
)

USER_NOT_EXIST = HTTPException(status_code=400, detail="User does not exist")

USER_INCORRECT_PERMISSIONS = HTTPException(
    status_code=401,
    detail="User does not have correct permissions",
)

USER_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

USER_INACTIVE = HTTPException(status_code=400, detail="Inactive user")
