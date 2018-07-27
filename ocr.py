from aip import AipOcr
import ast
import json

from PyPDF2 import PdfFileWriter, PdfFileReader


""" 你的 APPID AK SK """
APP_ID = 'Example'
API_KEY = 'YOUR_API_KEY'
SECRET_KEY = 'YOUR_SECRET_KEY'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def ocr_processor(image):
    """ 调用通用文字识别, 图片参数为本地图片 """
    a = client.basicGeneral(image)
    result = ast.literal_eval(str(a))

    result = result['words_result']
    result = [x['words'] for x in result]
    result = '\n'.join(result)
    return result
