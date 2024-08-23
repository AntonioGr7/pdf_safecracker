# PDF Safe Cracker
PDF Safecracker is an application that allows you to extract information such as tables, titles, and paragraphs from even very complex formats in a precise and reliable manner.

## Prerequisites

Before running the script, ensure that you have the following installed on your system in order to download LayoutDetection Model. 

- **Git**: Version control system.
- **Git LFS**: Git extension for versioning large files.

You can install Git and Git LFS using the following commands:

```bash
# Install Git
sudo apt-get update
sudo apt-get install git

# Install Git LFS
sudo apt-get install git-lfs
git lfs install
```

## Downloading the Model

To download the Layout Model open a terminal in the main folder and run 

```bash
chmod +x download_model.sh
./download_model.sh
```

If you have now a folder called 'models' with the model inside you are good to go.

## Get started 

You can find and example on how to use the class directly on a pdf in the file 'main.py'

```python
import os
from core.layout import PdfExtraction
from utils import load_pdf



if __name__ == "__main__":
    extractor = PdfExtraction()
    images = load_pdf("TSLA-Q2-2024-Update.pdf")
    results = extractor.run(images[3])

    print(results)
```