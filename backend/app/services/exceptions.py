class AuthError(Exception):
    pass


class EmailAlreadyRegistered(AuthError):
    pass


class InvalidCredentials(AuthError):
    pass
