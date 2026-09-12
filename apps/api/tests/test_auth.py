from pulseforge.config import Settings
from pulseforge.domain.auth import Principal, WorkspaceRole
from pulseforge.security.auth import issue_access_token
import jwt


def test_local_access_token_contains_workspace_roles():
    settings = Settings(jwt_secret="test-secret")
    principal = Principal(
        user_id="u1",
        email="u@example.com",
        workspace_roles={"ai-industry": WorkspaceRole.ADMIN},
    )
    token = issue_access_token(principal, settings)
    payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    assert payload["sub"] == "u1"
    assert payload["roles"]["ai-industry"] == "admin"
