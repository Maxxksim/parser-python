from config.setting_config import Settings


class ProxyConfig(Settings):
    proxy_username: str
    proxy_password: str

    proxy_list: list = [
        "disp.oxylabs.io:8001",
        "disp.oxylabs.io:8002",
        "disp.oxylabs.io:8003",
        "disp.oxylabs.io:8004",
        "disp.oxylabs.io:8005",
        "disp.oxylabs.io:8006",
        "disp.oxylabs.io:8007",
        "disp.oxylabs.io:8008",
        "disp.oxylabs.io:8008",
        "disp.oxylabs.io:8010",
    ]
