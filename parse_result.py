import pandas
from mindee import Client
from mindee.documents import TypeFinancialDocumentV1
import re

def parse_results(result):
    document_details = {}
    # To get the customer name (string)
    customer_name = result.document.customer_name.value
    if customer_name:
        document_details.update({'customer_name':customer_name})
    else:
        document_details.update({'customer_name':None})

    # To get the customer address (string)
    customer_address = result.document.customer_address.value
    if customer_address:
        document_details.update({'customer_address':customer_address})
    else:
        document_details.update({'customer_address':None})


    # To get the supplier name
    supplier_name = result.document.supplier_name.value
    if supplier_name:
        document_details.update({'supplier_name':supplier_name})
    else:
        document_details.update({'supplier_name':None})


    # To get the supplier address
    supplier_address = result.document.supplier_address.value
    if supplier_address:
        document_details.update({'supplier_address':supplier_address})
    else:
        document_details.update({'supplier_address':None})


    # customer_company_registrations = result.document.customer_company_registrations
    # if customer_company_registrations:
    #     document_details.update({'customer_company_registrations':customer_company_registrations})
    # else:
    #     document_details.update({'customer_company_registrations':None})
        
        
    # To get the list of customer numbers
    customer_company_registrations = result.document.customer_company_registrations
    customer_reg_val = []
    # Loop on each object
    for customer_registration in customer_company_registrations:
        # company_registration_type = customer_registration.type
        customer_registration_value = customer_registration.value
        customer_reg_val.append(customer_registration_value)
    if len(customer_reg_val) > 0:
        document_details.update({'customer_registration_value':customer_reg_val})
    else:
        document_details.update({'customer_registration_value':None})


    due_date = result.document.due_date.value
    if due_date:
        document_details.update({'due_date':due_date})
    else:
        document_details.update({'due_date':None})


    language = result.document.locale.value
    if language:
        document_details.update({'language':language})
    else:
        document_details.update({'language':None})


    currency = result.document.locale.currency
    if currency:
        document_details.update({'currency':currency})
    else:
        document_details.update({'currency':None})


    # To get the list of payment details
    reference_numbers = result.document.reference_numbers
    ref_num = []
    for reference_number in reference_numbers:
        ref_num.append(reference_number.value)
    if ref_num:
        document_details.update({'reference_number':ref_num})
    else:
        document_details.update({'reference_number':None})



    # To get the list of company numbers
    supplier_company_registrations = result.document.supplier_company_registrations
    comp_reg_val = []
    # Loop on each object
    for company_registration in supplier_company_registrations:
        company_registration_type = company_registration.type
        company_registration_value = company_registration.value
        comp_reg_val.append(company_registration_value)
    if len(comp_reg_val) > 0:
        document_details.update({'company_registration_value':comp_reg_val})
    else:
        document_details.update({'company_registration_value':None})


    # To get the total amount including taxes value (float), ex: 14.24
    total_amount = result.document.total_amount.value
    if total_amount:
        document_details.update({'total_amount':total_amount})
    else:
        document_details.update({'total_amount':None})



    # To get the total amount excluding taxes value (float), ex: 10.21
    total_net = result.document.total_net.value
    if total_net:
        document_details.update({'total_net':total_net})
    else:
        document_details.update({'total_net':None})



    # To get the total tax amount value (float), ex: 8.42
    total_tax = result.document.total_tax.value
    if total_tax:
        document_details.update({'total_tax':total_tax})
    else:
        document_details.update({'total_tax':None})


    line_items = []
    col = ['description', 'product_code', 'quantity', 'tax_amount', 'tax_rate', 'total_amount', 'unit_price']
    for lines in result.document.line_items:
        d = {}
        for i in col:
            extract = getattr(lines, i, None)
            d[i] = extract
        line_items.append(d)
    
    result = {}
    result.update({'document_details':document_details})
    result.update({'line_items':line_items})

    return result





def merge_dicts(dict1, dict2):
    result = dict(dict1)  # Create a copy of dict1 to avoid modifying it in place
    
    for key, value in dict2.items():
        if key in result:
            # If the key already exists in result, append the value to a list
            if isinstance(result[key], list):
                result[key].append(value)
            else:
                result[key] = [result[key], value]
        else:
            # If the key doesn't exist in result, simply add it
            result[key] = value

    return result





def getKeyValue(result):
    def get_all_key_value_pairs(data, parent_key='', pairs=None):
        if pairs is None:
            pairs = []

        if isinstance(data, dict):
            for key, value in data.items():
                new_key = parent_key + '.' + key if parent_key else key
                if isinstance(value, (dict, list)):
                    get_all_key_value_pairs(value, new_key, pairs)
                else:
                    pairs.append((new_key, value))
        elif isinstance(data, list):
            for index, item in enumerate(data):
                new_key = parent_key + f'[{index}]'
                if isinstance(item, (dict, list)):
                    get_all_key_value_pairs(item, new_key, pairs)
                else:
                    pairs.append((new_key, item))
        else:
            pairs.append((parent_key, data))
        
        return pairs


    # Get all key-value pairs
    pairs = get_all_key_value_pairs(result)

    # Print the key-value pairs
    result = []
    for key, value in pairs:
        key = key.replace('document_details.',"").replace('[',"").replace(']',"").replace('.',"_").replace('line_items',"")
        result.append((key,value))
    return result





def dataToTable(data):
    file_data = []
    table_data = {}
    for i in data:
        pattern = re.compile(r'^\d+')

        matches = pattern.findall(i[3])

        # If matches are found, take the first one (start integer)
        if matches:
            start_integer = int(matches[0])
            key = i[3].replace(f"{start_integer}_",'')

            if start_integer in table_data.keys():
                table_data[start_integer].update({key:i[4]})
            else:
                table_data.update({start_integer:{key:i[4]}})
        else:
            file_data.append((i[3], i[4]))

    line_items = []
    for k,v in table_data.items():
        line_items.append(v)
        
    return file_data, line_items

