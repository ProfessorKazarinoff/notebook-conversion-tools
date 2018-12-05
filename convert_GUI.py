# -*- coding: utf-8 -*-
"""
convert_GUI.py

This script produces a GUI window that converts Jupyter notebooks into different formats
Created on Wed Dec  5 10:26:57 2018

@author: peter.kazarinoff
"""

from gooey import Gooey, GooeyParser


@Gooey(dump_build_config=True, program_name="Notebook Conversion Tool")
def main():
    desc = "A Python GUI App to convert Jupyter Notebooks to other formats"
    file_help_msg = "Name of the Jupyter notebook file (.ipynb-file) you want to process"

    my_parser = GooeyParser(description=desc)
    my_parser.add_argument("Notebook_to_Convert", help=file_help_msg, widget="FileChooser")
    my_parser.add_argument("Output_Directory", help="Directory to save output", widget="DirChooser")
    my_parser.add_argument("Template_File", help=file_help_msg, widget="FileChooser")

    args = my_parser.parse_args()
    print(f'input file{args.Notebook_to_Convert}')
    print(f'output directory {args.Output_Directory}')
    print(f'template file {args.Template_File}')


if __name__ == "__main__":
    main()
