import os

import jwt

from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer

KEYCLOAK_URL = os.getenv("FASTAPI_APP_KEYCLOAK_URL")
KEYCLOAK_REALM = os.getenv("FASTAPI_APP_KEYCLOAK_REALM")
JWKS_URI = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs"
REPORTS_USER_ROLE = "prothetic_user"

jwks_client = jwt.PyJWKClient(JWKS_URI)

bearer_scheme = HTTPBearer()


def check_auth_user(token: str = Security(bearer_scheme)) -> dict[str, str] | None:
    return verify_auth_user(token.credentials)


def verify_auth_user(creds: str) -> dict[str, str] | None:
    try:
        signing_keys = jwks_client.get_signing_keys()
        assert len(signing_keys) == 1, "Invalid signing keys"
        key = signing_keys[0].key

        payload = jwt.decode(creds, key, algorithms=["RS256"])
        roles = payload.get("realm_access", {}).get("roles", [])

        if REPORTS_USER_ROLE not in roles:
            raise HTTPException(status_code=403, detail="User is not authorized to perform this action")

        return payload

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
