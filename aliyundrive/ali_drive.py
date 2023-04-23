import logging
from aligo import Aligo
from aligo.types.Enum import CheckNameMode
from aligo.types.BaseFile import BaseFile
from aligo.response.CreateFileResponse import CreateFileResponse
from aligo.request import MoveFileRequest
from aligo.response import MoveFileResponse
from aligo.response import MoveFileToTrashResponse

aligo = Aligo(level=logging.INFO)

def get_file_by_path(path: str = '/', parent_file_id: str = 'root',
                         check_name_mode: CheckNameMode = 'refuse',
                         drive_id: str = None): # type: ignore
    """根据路径获取云盘文件对象, 先找到啥就返回啥（早期可能存在同名文件（夹）），否则返回None

    Args:
        path: [str] 路径，无需以'/'开头
        parent_file_id: Optional[str] 父文件夹ID，默认为根目录，意思是基于根目录查找
        check_name_mode: Optional[CheckNameMode] 检查名称模式，默认为 'refuse'
        drive_id: Optional[str] 存储桶ID

    Returns:
        [BaseFile] 文件对象，或 None
    """    
    return aligo.get_file_by_path(path,parent_file_id,check_name_mode,drive_id)

def get_folder_by_path( path: str = '/', parent_file_id: str = 'root', create_folder: bool = False,
            check_name_mode: CheckNameMode = 'refuse', drive_id: str = None) -> BaseFile | CreateFileResponse | None: # type: ignore
    """根据文件路径，获取网盘文件对象

    Args:
        path: [str] 完整路径，无需以 '/' 开始或结束
        parent_file_id: Optional[str] 父文件夹ID，默认为根目录，意思是基于根目录查找
        create_folder:  Optional[bool] 不存在是否创建，默认：True. 此行为效率最高
        check_name_mode: Optional[CheckNameMode] 检查名称模式，默认为 'refuse'
        drive_id: Optional[str] 存储桶ID，一般情况下，drive_id 参数都无需提供

    Returns:
        文件对象，或创建文件夹返回的对象，或 None
    """    
    return aligo.get_folder_by_path(path,parent_file_id,create_folder,check_name_mode,drive_id)

def get_file(file_id: str, drive_id: str = None): # type: ignore
    """获取文件/文件夹

    Args:
        file_id: [str] 文件ID
        drive_id: Optional[str] 存储桶ID
    
    Returns:
        [BaseFile] 文件对象
    """    
    return aligo.get_file(file_id)    

def get_file_list(parent_file_id:str = 'root',drive_id: str = None, **kwargs): # type: ignore
    """获取文件列表

    Args:
        parent_file_id: Optional[str] 文件夹ID，默认为根目录
        drive_id: Optional[str] 存储桶ID
        kwargs: [dict] 其他参数

    Returns:
        [List[BaseFile]] 文件列表
    """    
    return aligo.get_file_list(parent_file_id,drive_id,**kwargs)



def move(file_id: str = None, # type: ignore
                  to_parent_file_id: str = 'root',
                  new_name: str = None, # type: ignore
                  drive_id: str = None, # type: ignore
                  to_drive_id: str = None, # type: ignore
                  **kwargs):
    """移动文件/文件夹

    Args:
        file_id: [必选] 文件/文件夹ID
        to_parent_file_id: [可选] 目标文件夹ID 默认移动到 根目录
        new_name: [可选] 新文件名
        drive_id: [可选] 文件所在的网盘ID
        to_drive_id: [可选] 目标网盘ID
        kwargs: [可选] 其他参数
    Returns: 
        [MoveFileResponse]
    """  
    return aligo.move_file(file_id,to_parent_file_id,new_name,drive_id,to_drive_id,**kwargs)

def move_to_trash(file_id: str, drive_id: str = None) -> MoveFileToTrashResponse: # type: ignore
    """移动文件到回收站

    Args:
        file_id: [必须] 文件ID
        drive_id: [可选] 文件所在的网盘ID

    Returns:
        [MoveFileToTrashResponse]
    """    
    return aligo.move_file_to_trash(file_id,drive_id)


def rename(file_id: str,
                    name: str,
                    check_name_mode: CheckNameMode = 'refuse',
                    drive_id: str = None): # type: ignore
    """文件/文件夹重命名

    Args:
        file_id: [必选] 文件id
        name: [必选] 新的文件名
        check_name_mode: [可选] 检查文件名模式
        drive_id: [可选] 文件所在的网盘id

    Returns:
        _type_: [BaseFile] 文件信息
    """    
    return aligo.rename_file(file_id,name,check_name_mode,drive_id)


if __name__ == '__main__':
    # hosts =  get_file_by_path('hosts.txt')
    # folder = get_folder_by_path('movieset') 
    # assert hosts is not None
    # assert folder is not None
    # res:MoveFileResponse = move_file(file.file_id,folder.file_id)
    # move(test_folder.file_id,folder.file_id)
    # move_to_trash(test_folder.file_id)
    # rename(hosts.file_id,'ssd.txt')
    pass
