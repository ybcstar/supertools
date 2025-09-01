import socket, threading, requests, json
from plugin_system.container import Container

class NetService:
    """极简网络工具箱"""
    @staticmethod
    def tcp_echo(host="127.0.0.1", port=9001):
        """启动一个 TCP 回显服务器（非阻塞）"""
        def _accept():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((host, port))
                s.listen()
                while True:
                    conn, addr = s.accept()
                    threading.Thread(target=lambda c: (
                        c.sendall(c.recv(1024)), c.close()
                    ), args=(conn,), daemon=True).start()
        threading.Thread(target=_accept, daemon=True).start()
        print(f"TCP echo on {host}:{port}")

    @staticmethod
    def http_get(url, **kw):
        """requests.get 的薄包装"""
        return requests.get(url, timeout=5, **kw).text

Container.register("net", NetService)