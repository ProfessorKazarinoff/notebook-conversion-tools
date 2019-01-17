# unzip_D2L.py
"""
A script to unzip and rename all of the assignments that are downloaded from D2L in an block
from D. Krugar 01/2018
"""

import os
import zipfile
from pathlib import Path
from gooey import Gooey, GooeyParser
import re

def unzip_dot_zip(infile_path,outfile_dir):
    """

    :param infile_path: pathlib.Path object. The full file path to the .zip archive which will be unzipped
    :param outfile_dir: pathlib.Path object. The full file path to the output directory where unzipped files will go
    :return:
    """
    zf = zipfile.ZipFile(infile_path, 'r')
    zf.extractall(outfile_dir)
    zf.close()

def unzip_rename(file_path, file_ext, zip_file, del_old):
    """
    :param file_path: directory where zip file is and will be unzipped to
    :param file_ext: file extension of the files of interest (do not include period)
    :param zip_file: zip file's filename (do not include .zip)
    :param del_old: (boolean) if True it will first delete all files with extension
        file_ext before unzipping zip_file.

    1) Deletes all files with file extension file_ext within the file_path dir
    2) Unzips the .zip archive with file name zip_file into file_path
    3) Renames all newly unzipped files to delete up to an including the first period in file name
        The Regex used w/Renameit.exe -->>   ^(.*?)\.

    zip_file must already be in the file_path dir
    """
    if del_old:
        # Delete existing files with file_ext extension
        delete_files(file_path, file_ext)

    # unzip zip file
    zfname = file_path + '\\' + zip_file + '.zip'
    zf = zipfile.ZipFile(zfname, 'r')  # must import zipfile first
    zf.extractall(file_path)
    zf.close()

    # delete pesky .htm(l) file(s)
    delete_files(file_path, 'htm')
    delete_files(file_path, 'html')

    # Rename new files
    rename_files_start_w_last_name(file_path, file_ext)
    # for lab 5 only
    rename_files_start_w_last_name(file_path, 'wav')  # for audio lab
    rename_files_start_w_last_name(file_path, 'pdf')  # for pseudocode
    pass

def delete_files(file_path, file_ext):
    """
    Delete files in specified path with matching extension
    :param file_path:
    :param file_ext:
    :return:
    """

    # Delete existing files with file_ext extension
    for name in os.listdir(file_path):
        if name.endswith("." + file_ext):
            os.remove(file_path +  '\\' + name)
    return

def rename_files_start_w_last_name(output_dir, file_ext):
    """
    Rename files in specified path with matching extension
    :param file_path:
    :param file_ext:
    :return:
    """

    for name in os.listdir(output_dir):  # must import os first
        # assumes that file already renamed if it starts with letter
        if name.endswith("." + file_ext) and name[0].isdigit():
            old_f_path = Path(output_dir, name)
            # deletes up to and including first .
            new_fname = Path(output_dir, re.sub('^(.*?)\.', '', name))
            os.rename(old_f_path, new_fname)
    return

@Gooey(dump_build_config=True, program_name="Unzip and rename files from D2L")
def main():
    desc = "A Python GUI App to convert a .zip archive downloaded from D2L to one folder. Also renames the files with student's last name"
    zip_select_help_msg = "Select a .zip archive to process"
    file_extension_help_msg = "input the file extension you want to convert the names of. Do not include . just extension"

    my_parser = GooeyParser(description=desc)
    my_parser.add_argument(
        "zip_to_convert", help=zip_select_help_msg, widget="FileChooser"
    )
    my_parser.add_argument(
        "file_extension_to_rename", help=file_extension_help_msg, widget="FileChooser"
    )
    my_parser.add_argument(
        "Output_Directory", help="Directory to save output", widget="DirChooser"
    )


    args = my_parser.parse_args()
    zip_file_path = Path(args.zip_to_convert)
    output_dir = Path(args.Output_Directory)
    extension = args.file_extension_to_rename
    unzip_dot_zip(zip_file_path, output_dir)
    rename_files_start_w_last_name(output_dir, extension)
    #zip_file_path = Path(args.Input_Directory)
    #zip_file = zip_file_path.stem
    #unzip_rename(args.Input_Directory, 'ipynb', zip_file, False)
    """
    :param file_path: directory where zip file is and will be unzipped to
    :param file_ext: file extension of the files of interest (do not include period)
    :param zip_file: zip file's filename (do not include .zip)
    :param del_old: (boolean) if True it will first delete all files with extension
        file_ext before unzipping zip_file.

    1) Deletes all files with file extension file_ext within the file_path dir
    2) Unzips the .zip archive with file name zip_file into file_path
    3) Renames all newly unzipped files to delete up to an including the first period in file name
        The Regex used w/Renameit.exe -->>   ^(.*?)\.

    zip_file must already be in the file_path dir
    """

    print()
    print(f"input zip archive \n {args.zip_to_convert}")
    print()
    print(f"output directory \n {args.Output_Directory}")
    print()


if __name__ == "__main__":
    main()