from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...





import socket





class XIp:
    ROUTER     = "192.168.0.1"
    LAPTOP     = "192.168.0.25"
    TELEVISION = "192.168.0.96"
    DESKTOP    = "192.168.0.104"
    MOBILE     = "192.168.0.230" 
    LOCALHOST  = "127.0.0.1"

    LOCALIPS   = [ROUTER, LAPTOP, DESKTOP, MOBILE, TELEVISION]


    @classmethod
    def iam(cls):
        localip = cls.ip()
        device = "UNKNOWN"
        if localip == cls.ROUTER:
            device = "ROUTER"
        elif localip == cls.LAPTOP:
            device = "LAPTOP"
        elif localip == cls.DESKTOP:
            device = "DESKTOP"
        elif localip == cls.MOBILE:
            device = "MOBILE"
        elif localip == cls.TELEVISION:
            device = "TELEVISION"
        
        return device
        

    @classmethod
    def ip(cls):
        ips = []
        try:
            hostname = socket.gethostname()
            ips.extend(socket.gethostbyname_ex(hostname)[2])
        except Exception:
            ...

        try:
            infos = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET, socket.SOCK_STREAM)
            for info in infos:
                ip = info[4][0]
                if ip not in ips:
                    ips.append(ip)
        except Exception:
            ...

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            ip = sock.getsockname()[0]
            sock.close()
            if ip not in ips:
                ips.insert(0, ip)
        except Exception:
            ...

        for ip in ips:
            ip:str = ip
            if ip in cls.LOCALIPS:
                return ip

        for ip in ips:
            ip:str = ip
            if ip and not ip.startswith("127."):
                return ip

        return cls.LOCALHOST
    


if __name__ == "__main__":
    print(XIp.iam())
    print(XIp.ip())