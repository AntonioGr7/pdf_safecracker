import os
from core.layout import PdfExtraction
from utils import load_pdf



if __name__ == "__main__":
    extractor = PdfExtraction()
    images = load_pdf("TSLA-Q2-2024-Update.pdf")
    results = extractor.run(images[3])

    print(results)