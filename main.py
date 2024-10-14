from mindee import Client
from mindee.documents import TypeFinancialDocumentV1
from pdf_to_img import parse_pdf
from parse_result import parse_results, merge_dicts
import re

def parse_images(file_name):
    mindee_client = Client(api_key="")    #please put your mindee api key hrer.
    input_doc = mindee_client.doc_from_path(file_name)
    result = input_doc.parse(TypeFinancialDocumentV1)
    # print(result.document)
    result = parse_results(result)
    return result



def check_filetype(file_name):
    print(file_name)
    if re.findall('.jpg|.jpeg|.png',file_name):
        result = parse_images(file_name)
        # print(result)
        return result

    elif '.pdf' in file_name:
        result = {}
        all_images = parse_pdf(file_name)
        for img in all_images:
            _result = parse_images(file_name)
            result = merge_dicts(result, _result)
        return result

    else:
        print('Invalid File Type')
        return {}


# #Example images
# file_name = 'C:/Users/rvarma/Pictures/ZU1-ZNUS-159318.jpg'
# file_name2 = 'C:/Users/rvarma/Pictures/img.png'
# file_name3 = 'C:/Users/rvarma/Pictures/img2.png'
# #Example pdf
# file_name4 = 'C:/Users/rvarma/Downloads/ZU1-ZNUS-159318.pdf'

# res = check_filetype(file_name)
# print(res)