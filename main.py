import os
import glob

from pdf_util import pdf_splitter, merger


if __name__ == '__main__':
    while True:
        print('请选择：')
        print('1.按目录拆分')
        print('2.按页拆分')
        print('3.合并pdf')
        print('4.退出')
        option = input('请输入数字并回车')

        if option == '1':
            pass
        elif option == '2':
            pdf_path = input('请输入文件路径：')
            pdf_splitter(pdf_path)
            print('按页拆分完成')
            pass
        elif option == '3':
            pdfs_path = input('请输入pdf文件文件夹路径（最后以/结尾）：')
            in_path = f'{pdfs_path}*.pdf'
            paths = glob.glob(in_path)
            sorted_paths = sorted(paths, key=lambda i: int(os.path.splitext(os.path.basename(i))[0]))
            merger(f'{pdfs_path}merged.pdf', sorted_paths)
            print('合并PDF完成')
            pass
        else:
            print('退出')
            break