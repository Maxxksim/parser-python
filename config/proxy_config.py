from config.setting_config import Settings


class ProxyConfig(Settings):
    proxy_username: str
    proxy_password: str

    proxy_list: list = [
        "http://45.38.107.97:6014",
        "http://64.137.96.74:6641",
        "http://198.23.243.226:6361",
        "http://38.154.185.97:6370",
        "http://84.247.60.125:6095",
        "http://191.96.254.138:6185",
        "http://198.46.161.42:5092",
        "http://64.137.10.153:5803",
        "http://104.164.49.38:7693",
        "http://23.26.71.145:5628",
    ]
