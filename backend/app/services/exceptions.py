class AuthError(Exception):
    pass


class EmailAlreadyRegistered(AuthError):
    pass


class InvalidCredentials(AuthError):
    pass


class InvalidGoogleToken(AuthError):
    pass

class EventError(Exception):
    pass


class EventNotFound(EventError):
    pass


class EventInvalidStatus(EventError):
    pass


class RegistrationError(Exception):
    pass


class RegistrationAlreadyExists(RegistrationError):
    pass


class RegistrationNotAllowed(RegistrationError):
    pass
