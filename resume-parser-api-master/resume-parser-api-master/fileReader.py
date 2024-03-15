import glob
import os

import pandas as pd

from fileParser import fileParser


def fileReader(inputPath):
    Resume_Vector = []
    Ordered_list_Resume = []
    Ordered_list_Resume_Score = []
    LIST_OF_FILES = []
    LIST_OF_FILES_PDF = []
    LIST_OF_FILES_DOC = []
    LIST_OF_FILES_DOCX = []
    Resumes = []

    os.chdir(inputPath)
    for file in glob.glob('**/*.pdf', recursive=True):
        LIST_OF_FILES_PDF.append(file)
    for file in glob.glob('**/*.doc', recursive=True):
        LIST_OF_FILES_DOC.append(file)
    for file in glob.glob('**/*.docx', recursive=True):
        LIST_OF_FILES_DOCX.append(file)

    LIST_OF_FILES = LIST_OF_FILES_DOC + LIST_OF_FILES_DOCX + LIST_OF_FILES_PDF
    print(LIST_OF_FILES)

    # parsedresume = pd.DataFrame()
    concatenated_dfs = []
    for j,i in enumerate(LIST_OF_FILES):
        Temp = i.split(".")
        if Temp[1] == "pdf" or Temp[1] == "Pdf" or Temp[1] == "PDF":
            try:
                print("This is PDF File" , i)
                parsedSingleResume = fileParser(i)
                parsedSingleResume['fileName'] = i

                concatenated_dfs.append(parsedSingleResume)
            except Exception as e: print(e)

        if Temp[1] == "txt" or Temp[1] == "Txt" or Temp[1] == "TXT":
            print("This is TXT" , i)

            try:
                parsedSingleResume = fileParser(i)
                parsedSingleResume['fileName'] = i

                concatenated_dfs.append(parsedSingleResume)
            except Exception as e: print(e)

        if Temp[1] == "docx" or Temp[1] == "Docx" or Temp[1] == "DOCX":
            print("This is DOCX" , i)

            try:
                parsedSingleResume = fileParser(i)
                parsedSingleResume['fileName'] = i

                concatenated_dfs.append(parsedSingleResume)
            except Exception as e: print(e)

    print(pd.concat(concatenated_dfs))
    return pd.concat(concatenated_dfs)

