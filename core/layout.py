from layoutlmv3.model_init import Layoutlmv3_Predictor
from core.table import StructTable
from paddleocr import PaddleOCR
from config import read_configuration
import os
import yaml
import torch
import cv2

import torch

class PdfExtraction():
    def __init__(self):
        configuration_path = os.getcwd()+"/config/config.yaml"
        configuration = read_configuration(configuration_path)
        self.device = configuration["device"]

        self.layout_model_path = configuration["models"]["layout"]["weight_path"]
        self.layout_configuration_path = configuration["models"]["layout"]["config_path"]
        self.layout_model = Layoutlmv3_Predictor(self.layout_model_path,self.layout_configuration_path,eval_only=True)

        self.layout_map = {"title":0,"plain_text":1,"abandon":2,"figure":3,
                           "figure_caption":4,"table":5,"table_caption":6,
                           "table_footnote":7,"isolate_formula":8,"formula_caption":9}
        self.reverse_layout_map = {v:k for k,v in self.layout_map.items()}
        ### Category are the following
        # "title":0
        # "plain text":1
        # "abandon":2
        # "figure":3
        # "figure_caption":4
        # "table":5 
        # "table_caption":6
        #  "table_footnote":7
        # "isolate_formula":8
        # "formula_caption":9

        self.max_new_tokens = configuration["models"]["table_extraction"]["max_new_tokens"]
        self.max_waiting_time = configuration["models"]["table_extraction"]["max_time"]
        self.table_extraction_model = StructTable(max_new_tokens=self.max_new_tokens,max_time=self.max_waiting_time).to(self.device)

        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')

    def run(self,image):
        layout = self.extract_layout(image)
        layout = self.extract(image,layout)
        return layout

    def extract_layout(self,image):
        layout_res = self.layout_model(input_image, ignore_catids=[])
        return layout_res
    
    def extract(self,image,layout):
        elements = self.__crop(image,layout)
        for e in elements:
            if e['category_id'] == self.layout_map['table']:
                with torch.no_grad():
                    output = self.table_extraction_model(e['crop'])
                    e['text']= output
            elif e['category_id'] == self.layout_map['figure']:
                continue
            else:
                t = np.asarray(e['crop'])
                results = self.ocr.ocr(t)
                output = ""
                try:
                    if results[0] is not None:
                        for r in results[0]:
                            output += r[1][0] + " "
                        e['text'] = output
                except Exception as e:
                    print("Something wrong with this element")
        return elements

    
    def __crop(self,image,page_layout):
        pil_img = Image.fromarray(cv2.cvtColor(input_image, cv2.COLOR_RGB2BGR))
        cropped_images = []
        page = page_layout['layout_dets']
        for element in page:
            xmin, ymin = int(element['poly'][0]), int(element['poly'][1])
            xmax, ymax = int(element['poly'][4]), int(element['poly'][5])
            crop_box = [xmin, ymin, xmax, ymax]
            cropped = pil_img.convert("RGB").crop(crop_box)
            element['crop'] = cropped
        return page
