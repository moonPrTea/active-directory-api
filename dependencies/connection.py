import socket
import ssl
from ldap3 import ALL, Server, Connection, Tls

import ssl
import socket

from . import ldap_settings


class LDAPConnection:
    def __init__(self):
        self.address = ldap_settings.ADRESS
        self.port = ldap_settings.PORT
        self.username = ldap_settings.USERNAME
        self.password = ldap_settings.PASSWORD
        self.server = None
        self.connecter = None
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
            self.connecter = Connection(
                self.server, 
                user=self.username, 
                password=self.password,
                auto_bind=True, 
                receive_timeout=60, 
                pool_keepalive=60,
                client_strategy='SAFE_RESTARTABLE'
            )
            
            if self.connecter.bound:
                print('Соединение установлено')
                self._socket = self.connecter.socket
                if self._socket:
                    print(f"SSL соединение: {isinstance(self._socket, ssl.SSLSocket)}")
                    print('Сокет живет, на этом спасибо')
                    self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                    self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
                    self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
                    self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
                
                if isinstance(self._socket, ssl.SSLSocket):
                    print("SSL соединение активно")
                else:
                    print("Ошибка: сокет не SSL, отсюда начинаются проблемы")

            else:
                print('Не удалось установить соединение')
                
        except Exception as e:
            print(f'Ошибка при подключении: {e}')
            raise

    @property
    def connection(self):
        if not self.is_active_connection():
            self._reconnect()
        return self.connecter
    
    def _reconnect(self):
        try:
            if self.connecter:
                self.connecter.unbind()
            self._initialize_connection()
            print("Переподключение успешно выполнено")
            return True, None
        except Exception as e:
            print(f'Ошибка при переподключении: {e}')
            return False, e
    
    def is_active_connection(self):
        if not self.connecter or not self.connecter.bound:
            return False
        
        try:
            self.connecter.search('', '(objectClass=*)', search_scope='BASE', attributes=['*'])
            return True
        except:
            return False
    


connecter = LDAPConnection()
ldap = connecter.connection