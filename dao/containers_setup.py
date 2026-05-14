from settings import settings
from dependencies import ldap


def create_all_containers():
    create_container(settings.ldap.USER_OU)
    create_container(settings.ldap.GROUP_OU)


def create_container(ou_name: str):
    ou_dn_address = f"OU={ou_name},{settings.ldap.BASE_DN}"
    ou_attributes = {
        "objectClass": ["top", "organizationalUnit"],
        "ou": ou_name
    }

    if ldap.add(ou_dn_address, attributes=ou_attributes):
        return {"success": True}

    return {"success": False, 'message': ldap.last_error}

