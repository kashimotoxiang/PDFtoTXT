import glob
import os
from joblib import Memory, Parallel, delayed
from PyPDF2 import PdfFileReader, PdfFileWriter
from wand.image import Image
from tqdm import tqdm
import lyx
from os.path import basename
from ocr import ocr_processor
FILEPATH = "sample.pdf"
memory = Memory(cachedir='./cache')


def split_pdf(filepath):
    inputpdf = PdfFileReader(open(filepath, "rb"))
    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        with open("tmp/%s.pdf" % str(i).zfill(3), "wb") as outputStream:
            output.write(outputStream)


@memory.cache
def get_blob(data):
    pages = data[0]
    item = data[1]
    image = Image(file=open(item, 'rb'), resolution=400)
    return (pages, image.make_blob('jpeg'))


def get_pdf():
    filename = glob.glob('./tmp/*.pdf')
    filename = sorted(filename)
    filename = [(basename(x), x) for x in filename]
    result = Parallel(n_jobs=4)(delayed(get_blob)(item) for item in filename)
    return result


def main():
    split_pdf(FILEPATH)
    image_blobs = get_pdf()
    for pages, image in image_blobs:
        __content = ocr_processor(image)
        print(pages)
        lyx.io.write_all(__content, 'txt/'+str(pages)+'.txt')


if __name__ == '__main__':
    main()
