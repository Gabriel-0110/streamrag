from __future__ import annotations
import os
import base64
import json
import urllib.parse

# Ensure .env is loaded
try:
    import src.env  # noqa: F401
except Exception:
    pass


def decode_jwt_meta(name: str):
    tok = os.getenv(name)
    if not tok:
        return {"name": name, "set": False}
    parts = tok.split(".")
    role = None
    ref = None
    if len(parts) >= 2:

        def pad(s: str) -> str:
            return s + "=" * ((4 - len(s) % 4) % 4)

        try:
            payload = json.loads(base64.urlsafe_b64decode(pad(parts[1])).decode())
            role = payload.get("role")
            ref = payload.get("ref")
        except Exception:
            role = "decode_error"
    return {"name": name, "set": True, "role": role, "ref": ref}


url = os.getenv("SUPABASE_URL") or ""
host = urllib.parse.urlparse(url).hostname or ""
url_ref = host.split(".")[0] if host else None

print({"SUPABASE_URL": url, "project_ref_from_url": url_ref})
for var in ("SUPABASE_SERVICE_ROLE_KEY", "SUPABASE_ANON_KEY", "SUPABASE_KEY"):
    print(decode_jwt_meta(var))
