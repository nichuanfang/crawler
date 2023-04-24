# 全局环境
import os
from my_selenium.my_selenium import logging

def get_environ(ENVIRON:str,default:str|int):
    """获取环境变量 并打印日志

    Args:
        ENVIRON (str): 环境变量
        default (_type_): 默认值

    Returns:
        _type_: 环境变量值
    """    
    ENV = os.environ.get(ENVIRON,'')    
    if ENV == '':
        logging.info(f'===========================未设置环境变量{ENVIRON} 使用默认值{default} =============================')  
        return default
    if isinstance(default,int):
        try:
            return int(ENV)
        except Exception as e: 
            logging.info(f'===========================环境变量{ENVIRON}数据类型错误,应该为int,采用默认值========================')    
            return default
    return ENV

# 环境 dev|test|prod
CRAWLER_ENV = get_environ('CRAWLER_ENV','dev')
# crawler域名 默认https 需要配置证书
CRAWLER_HOST = get_environ('CRAWLER_HOST','127.0.0.1')
# tinymediamanager通过http调用远程刮削需要的token 默认为''
TMM_API_KEY = get_environ('TMM_API_KEY','')
# tinymediamanager服务根路径
TMM_HOST = get_environ('TMM_HOST','www.vencenter.cn')
# IOS推送APP Bark的token     模板: https://api.day.app/{BARK_TOKEN}/{content}
BARK_TOKEN = get_environ('BARK_TOKEN','')


# 单例类
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Env(metaclass=Singleton):
    def __init__(self):
        # 初始化环境
        self.__switch_env__(CRAWLER_ENV)

    def __switch_env__(self,CRAWLER_ENV:str|int):
        if isinstance(CRAWLER_ENV,int):
            raise RuntimeError(f'环境变量:{CRAWLER_ENV}类型错误')
        # 开发
        if CRAWLER_ENV.lower() == 'dev':
            self.__switch_to_dev__()
        # 测试
        elif CRAWLER_ENV.lower() == 'test':
            self.__switch_to_test__()
        # 生产
        elif CRAWLER_ENV.lower() == 'prod':
            self.__switch_to_prod__()
        # 默认开发
        else:
            self.__switch_to_dev__()

    # 切换开发环境
    def __switch_to_dev__(self):
        self.curr_env = 'dev'
        # 默认域名/ip地址
        self.host = f'{CRAWLER_HOST}'
        # 默认监听地址
        self.listening_host = '127.0.0.1'
        # crawler根路径
        self.crawler_base_url = f'http://{self.host}:5000'
        # tmm根路径
        self.tmm_base_url = f'http://{TMM_HOST}:7878'
        # tmm刮削器http请求api-key
        self.tmm_api_key = TMM_API_KEY
    
    # 切换测试环境
    def __switch_to_test__(self):
        self.curr_env = 'test'
        # 默认域名/ip地址
        self.host = f'{CRAWLER_HOST}'
        # 默认监听地址
        self.listening_host = '127.0.0.1'
        # crawler根路径
        self.crawler_base_url = f'http://{self.host}:5000'
        # tmm根路径
        self.tmm_base_url = f'http://{TMM_HOST}:7878'
        # tmm刮削器http请求api-key
        self.tmm_api_key = TMM_API_KEY

    # 切换生产环境
    def __switch_to_prod__(self):
        self.curr_env = 'prod'
        # 默认域名/ip地址
        self.host = f'{CRAWLER_HOST}'
        # 默认监听地址
        self.listening_host = '0.0.0.0'
        # crawler根路径  
        self.crawler_base_url = f'https://{self.host}'
        # tmm根路径
        self.tmm_base_url = f'http://{TMM_HOST}:7878'
        # tmm刮削器http请求api-key 从环境变量中获取
        self.tmm_api_key = TMM_API_KEY