import os
import fitz
import numpy as np
from tqdm import tqdm
import time
from PIL import Image

def load_pdf(pdf_path, dpi=72):
    images = []
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        page = doc[i]
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
        image = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)

        # if width or height > 3000 pixels, don't enlarge the image
        if pix.width > 3000 or pix.height > 3000:
            pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
            image = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)

        # images.append(image)
        images.append(np.array(image)[:,:,::-1])
    return images

from pypandoc import convert_text

def convert_latex(tables,output_format=["html","markdown"]):
    outputs = {}
    for i, latex_code in enumerate(tables):
        for tgt_fmt in output_format:
            tgt_code = convert_text(latex_code, tgt_fmt, format='latex') if tgt_fmt != 'latex' else latex_code
            outputs[tgt_fmt]=tgt_code
    return outputs

import re
def latex_rm_whitespace(s: str):
    """Remove unnecessary whitespace from LaTeX code.
    """
    text_reg = r'(\\(operatorname|mathrm|text|mathbf)\s?\*? {.*?})'
    letter = '[a-zA-Z]'
    noletter = '[\W_^\d]'
    names = [x[0].replace(' ', '') for x in re.findall(text_reg, s)]
    s = re.sub(text_reg, lambda match: str(names.pop(0)), s)
    news = s
    while True:
        s = news
        news = re.sub(r'(?!\\ )(%s)\s+?(%s)' % (noletter, noletter), r'\1\2', s)
        news = re.sub(r'(?!\\ )(%s)\s+?(%s)' % (noletter, letter), r'\1\2', news)
        news = re.sub(r'(%s)\s+?(%s)' % (letter, noletter), r'\1\2', news)
        if news == s:
            break
    return s