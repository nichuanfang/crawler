# 全局环境

# 单例类
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Env(metaclass=Singleton):
    def __init__(self):
        pass

    # 切换开发环境
    def __switch_to_dev__(self):
        self.curr_env = 'dev'
        # 默认域名/ip地址
        self.host = '127.0.0.1'
        # 默认监听地址
        self.listening_host = '127.0.0.1'
        # 默认监听端口
        self.port = 5000
        # 默认协议
        self.protocol = 'http'
        # crawler根路径
        self.crawler_base_url = 'http://127.0.0.1:5000'
        # tmm根路径
        self.tmm_base_url = 'http://www.vencenter.cn:7878'
    
    # 切换测试环境
    def __switch_to_test__(self):
        self.curr_env = 'test'
        # 默认域名/ip地址
        self.host = '127.0.0.1'
        # 默认监听地址
        self.listening_host = '127.0.0.1'
        # 默认监听端口
        self.port = 5000
        # 默认协议
        self.protocol = 'http'
        # crawler根路径
        self.crawler_base_url = 'http://127.0.0.1:5000'
        # tmm根路径
        self.tmm_base_url = 'http://www.vencenter.cn:7878'

    # 切换生产环境
    def __switch_to_pro__(self):
        self.curr_env = 'prod'
        # 默认域名/ip地址
        self.host = 'crawler.vencenter.cn'
        # 默认监听地址
        self.listening_host = '0.0.0.0'
        # 默认端口
        self.port = 5000
        # 默认协议
        self.protocol = 'https'
        # crawler根路径
        self.crawler_base_url = 'https://crawler.vencenter.cn'
        # tmm根路径
        self.tmm_base_url = 'http://www.vencenter.cn:7878'