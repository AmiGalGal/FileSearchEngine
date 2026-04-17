#File purpose: parse a file (.pdf, .doc, .docx etc) into usable text
#allowed suffix: pdf, docx, txt, md

import os
import docx2txt
from pypdf import PdfReader

def DocToText(path):
    if os.path.exists(path):
        suffix = os.path.splitext(path)[1]
        if suffix == ".pdf":
            reader = PdfReader(path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        elif suffix == ".docx":
            return docx2txt.process(path)
        elif suffix == ".txt":
            with open(path, 'r', encoding='utf-8') as file:
                return file.read()
        elif suffix == ".md":
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return "File not supported"
    else:
        return "File Not Found"

