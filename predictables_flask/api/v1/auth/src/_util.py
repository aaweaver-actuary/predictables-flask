def check_password_hash(hashed_password: str, password: str) -> bool:
    """
    Check a password against a hashed password.

    Parameters
    ----------
    hashed_password : str
        The hashed password.
    password : str
        The password to check.

    Returns
    -------
    bool
        True if the password matches the hashed password. False otherwise.
    """
    return hashed_password == password
