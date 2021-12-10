import os
import glob
from pathlib import Path
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger


def split_by_sections(path):
    """按照pdf书签结构拆分pdf文件，目前只支持第一级目录拆分

    Args:
        path (str): pdf文件路径
    """

    # 获取文件名（不包含路径和后缀），以便作为拆分后的文件名的基础
    filename = os.path.splitext(os.path.basename(path))[0]

    pdf_reader = PdfFileReader(path)
    outlines = pdf_reader.outlines
    # 存储各个section信息，包括标题、起始页、结束页
    sections = []
    titles = []
    start_pages = []
    end_pages = []

    for outline in outlines:
        titles.append(outline['/Title'])
        start_pages.append(pdf_reader.getDestinationPageNumber(outline) + 1)
        # 结束页码取下一个section的起始页码-1
        # end_pages数组比其他数组多一个元素
        # 虽然此处是本section的起始页码-1，实际上从数组取值是从第二个开始取值的
        # 因此起始存储的是下一个section的起始页码-1
        last_section_page = pdf_reader.getDestinationPageNumber(outline)
        end_pages.append(last_section_page)
    end_pages.append(pdf_reader.numPages)
    for i in range(len(outlines)):
        # 将section信息存入数组
        section = [titles[i], start_pages[i], end_pages[i + 1]]
        sections.append(section)

    for idx, section in enumerate(sections):
        title = section[0]
        pdf_writer = PdfFileWriter()
        # 每个section分别存储到独立的pdf
        for i in range(section[2] - section[1] + 1):
            pdf_writer.addPage(pdf_reader.getPage(section[1] + i - 1))
        output_filename = f'{filename}-{idx + 1}-{title}.pdf'
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)


def pdf_splitter(path):
    """将pdf每一页拆分为单独的pdf文件

    Args:
        path (str): 拆分前的文件路径
    """
    fname = os.path.splitext(os.path.basename(path))[0]
    Path(fname).mkdir(parents=True, exist_ok=True)

    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        # output_filename = '{}_page_{}.pdf'.format(
        #     page+1, fname)
        output_filename = f'{fname}/{page + 1}.pdf'

        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)

        print('Created: {}'.format(output_filename))


def merger(output_path, input_paths):
    """将多个pdf合并为一个pdf

    Args:
        output_path (str): 合并后的pdf文件路径
        input_paths (str): 待合并的pdf路径（数组）
    """
    pdf_merger = PdfFileMerger()
    file_handles = []
    
    for path in input_paths:
        pdf_merger.append(path)
        
    with open(output_path, 'wb') as fileobj:
        pdf_merger.write(fileobj)


def merge_from_images(output_path, image_paths):
    """将多个图片合并为pdf文件

    Args:
        output_path (str): 合并后的pdf文件路径
        image_paths (str): 待生成pdf的图片路径（数组）
    """
    images = []
    for path in image_paths:
        im = Image.open(path)
        images.append(im)

    images[0].save(output_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])


if __name__ == '__main__':
    pass