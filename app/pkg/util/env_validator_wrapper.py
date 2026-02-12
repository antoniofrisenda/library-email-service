import os


def _get_env(env_var: str) -> str:
    var = os.getenv(env_var)
    if not var:
        raise RuntimeError(f"Missing required env var: {env_var}")
    return var
