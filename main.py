import os
from utils import load_pdf, convert_latex, latex_rm_whitespace
from core.layout import PdfExtraction



if __name__ == "__main__":
    extractor = PdfExtraction()
    images = load_pdf("TSLA-Q2-2024-Update.pdf")
    results = extractor.run(images[7])
    for r in results:
        if r['category_id'] == 5: ## 5 is Tables
            table = latex_rm_whitespace(r['text'][0])
            converted_table = convert_latex(tables=[table])
            print("Table:\n")
            print(converted_table['markdown'])
        else:
            if "text" in r:
                if r['category_id'] == 0: ## this is a title
                    print(f"## {r['text']}\n")
                elif r['category_id'] == 6: #table caption
                    print(f"Table: {r['text']}")
                else:
                    print(f"{r['text']}\n")
