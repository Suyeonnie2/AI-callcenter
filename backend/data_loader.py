import csv

def load_company_info(file_path):
    company_info = {}
    with open(file_path, mode='r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            company_info[row['key']] = row['value']
    return company_info

def load_user_intent(file_path):
    user_intent = {}
    with open(file_path, mode='r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            user_intent[row['intent']] = row['response']
    return user_intent