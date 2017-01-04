import socket

def is_remote_tcp_port_open(host, port, timeout=10):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        sock.connect((host, port))
        sock.close()
        return True
    except Exception as e:
        print(e)
        sock.close()
        return False

