from fastapi import Header, HTTPException

ADMIN_SECRET = "super-admin-secret"

def verify_admin(x_admin_secret: str = Header(None)):

    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")

    return True
