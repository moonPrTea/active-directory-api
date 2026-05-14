from settings import settings


def check_headers(headers):
    if headers.get('Authorization') == settings.token.AUTH_TOKEN.get_secret_value():
        return True

    return False
