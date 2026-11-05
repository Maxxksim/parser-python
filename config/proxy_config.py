from config.setting_config import Settings


class ProxyConfig(Settings):
    proxy_username: str
    proxy_password: str

    proxy_list: list = [
        "isp.oxylabs.io:8001",
        "isp.oxylabs.io:8002",
        "isp.oxylabs.io:8003",
        "isp.oxylabs.io:8004",
        "isp.oxylabs.io:8005",
        "isp.oxylabs.io:8006",
        "isp.oxylabs.io:8007",
        "isp.oxylabs.io:8008",
        "isp.oxylabs.io:8008",
        "isp.oxylabs.io:8010",
    ]
