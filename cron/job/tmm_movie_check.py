# 检测tmm/tmm-movies文件夹是否存在已刮削好的电影文件夹 有就移至movies文件夹
from aliyundrive import ali_drive
from aligo.types.BaseFile import BaseFile
import subprocess

# 指定时间后执行该检查
def tmm_movie_check():
    tmm_movies_folder = ali_drive.get_folder_by_path('tmm/tmm-movies')
    assert tmm_movies_folder is not None
    def callable(path:str,file:BaseFile):
        # 获取.mkv文件 
        if file.file_extension.lower() in ['mkv','mov','wmv','flv','avi','avchd','webm','mp4']:
            # 查看当前文件夹下是否有同名文件 
            flag = False
            for item in ali_drive.get_file_list(file.parent_file_id):
                if item.file_extension.lower() == 'nfo':
                    flag = True
                    break
            if flag:
                # 有nfo文件 直接将该电影文件夹移至movies文件夹
                move_to_movies(file.parent_file_id,tmm_movies_folder.file_id,[])
        return None

    ali_drive.aligo.walk_files(callable,tmm_movies_folder.file_id)
    # 关闭tinymediamanager
    print(subprocess.call('nsenter -m -u -i -n -p -t 1 sh -c "docker stop tinymediamanager"',shell=True))

def move_to_movies(parent_file_id:str,tmm_file_id:str,path_list:list):
    """递归文件夹 在movies创建电影文件夹

    Args:
        parent_file_id (str): 父文件id
        tmm_file_id (str): tmm文件夹id
        path_list (list): 路径列表
    """    
    if parent_file_id != tmm_file_id:
        file = ali_drive.get_file(parent_file_id)
        # 操作 
        path_list.append(file.name)
        move_to_movies(file.parent_file_id,tmm_file_id,path_list)
    else:
        # 分层级在movies中创建文件夹
        path_list.reverse()
        file_path = 'tmm/tmm-movies/'+'/'.join(path_list)
        base_path = 'movies'
        final_path = base_path
        final_path_dp = []
        for path in path_list:
            # 如果是最后一个元素 则移动第一个文件夹到final_path
            if path == path_list[-1]:
                src_file = ali_drive.get_folder_by_path(file_path)
                assert src_file is not None
                desc_file = ali_drive.get_folder_by_path(final_path)
                assert desc_file is not None
                ali_drive.move(src_file.file_id,desc_file.file_id)
                # 移除final_path_dp的空文件夹
                for dp in final_path_dp:
                    dp_file = ali_drive.get_folder_by_path(dp)
                    if dp_file is not None:
                        file_list = ali_drive.get_file_list(dp_file.file_id)
                        if len(file_list) == 0:
                            # 移除该文件夹
                            ali_drive.move_to_trash(dp_file.file_id)
                    pass
            final_path+='/'+path
            final_path_dp.append(final_path.replace('movies', 'tmm/tmm-movies'))
            folder = ali_drive.get_folder_by_path(final_path)
            if folder is None:
                ali_drive.aligo.create_folder(final_path)
        pass
    