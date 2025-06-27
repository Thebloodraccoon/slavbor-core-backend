from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
def login():
    return {"LOGIN": "TODO"}


@router.post("/logout")
def logout():
    return {"LOGOUT": "TODO"}


@router.post("/refresh")
def refresh_tokens():
    return {"REFRESH_TOKENS": "TODO"}


@router.post("/register")
def register():
    return {"REGISTER": "TODO"}
