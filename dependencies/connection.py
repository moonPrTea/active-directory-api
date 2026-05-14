from ldap3 import ALL, Server, Connection, Tls

import ssl
import socket

from settings import settings


class LDAPConnection:
    def __init__(self):
        self.address = settings.ldap.HOST
        self.port = settings.ldap.PORT
        self.username = settings.ldap.USERNAME
        self.password = settings.ldap.PASSWORD.get_secret_value()
        self.server = None

        self.ldap_connection = None
        self._socket = None
        self._initialize_connection()
        
    def _initialize_connection(self):
        try:

            self.server = Server(
                self.address, 
                port=self.port, 
                tls=Tls(validate=ssl.CERT_NONE),
                get_info=ALL, 
                use_ssl=True,
            )
            self.ldap_connection = Connection(
                self.server, 
                user=self.username, 
                password=self.password,
                auto_bind=True, 
                receive_timeout=60, 
                pool_keepalive=60,
                client_strategy='SAFE_RESTARTABLE'
            )
            
            if self.ldap_connection.bound:
                self._socket = self.ldap_connection.socket

                if self._socket:
                    self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                    self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPALIVE, 60)
                    self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
                    self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
                
        except Exception as e:
            print(f'An error occurred while creating connection: {e}')
            raise

    @property
    def connection(self):
        if not self.is_active_connection():
            self._reconnect()
        return self.ldap_connection
    
    def _reconnect(self):
        try:
            if self.ldap_connection:
                self.ldap_connection.unbind()

            self._initialize_connection()
            return True, None

        except Exception as e:
            print(f'An error occurred in reconnection operation: {e}')
            return False, e
    
    def is_active_connection(self):
        if not self.ldap_connection or not self.ldap_connection.bound:
            return False
        
        try:
            self.ldap_connection.search('', '(objectClass=*)', search_scope='BASE', attributes=['*'])
            return True
        except:
            return False
    


ldap_connection = LDAPConnection()
ldap = ldap_connection.connection
