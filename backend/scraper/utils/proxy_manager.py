import random
import os

class ProxyManager:
    def __init__(self, proxy_list_path='backend/config/proxies.txt'):
        self.proxy_list = self.load_proxies(proxy_list_path)
        self.current = 0

    def load_proxies(self, path):
        try:
            with open(path, 'r') as file:
                proxies = [line.strip() for line in file if line.strip()]
            return proxies
        except FileNotFoundError:
            return []

    def get_proxy(self):
        if not self.proxy_list:
            return None
        proxy = self.proxy_list[self.current]
        self.current = (self.current + 1) % len(self.proxy_list)
        return proxy

    def rotate_proxy(self):
        if self.proxy_list:
            self.current = (self.current + 1) % len(self.proxy_list)
