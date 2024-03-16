from tika import parser
import re
import pandas as pd

def fileParser(file):
    # file = r'/content/sample_data/Resume.pdf'
    file_data = parser.from_file(file)
    text = file_data['content']
    # print(text)
    parsed_content = {}

    email = get_email_addresses(text)
    print(email)
    parsed_content['email'] = email

    phone_number= get_phone_numbers(text)
    if len(phone_number) <= 10:
        print(phone_number)
        parsed_content['Phone number'] = phone_number

    Keywords = ["technical skills",
                "skills",
                "position of responsibility",
                "responsibilities",
                "tech stack"
                ]

    text = text.replace("\n"," ")
    text = text.replace("[^a-zA-Z0-9]", " ");
    re.sub('\W+','', text)
    text = text.lower()
    # print(text)

    content = {}
    indices = []
    keys = []
    for key in Keywords:
        try:
            content[key] = text[text.index(key) + len(key):]
            indices.append(text.index(key))
            keys.append(key)
        except:
            pass

    #Sorting the indices
    zipped_lists = zip(indices, keys)
    sorted_pairs = sorted(zipped_lists)
    sorted_pairs

    tuples = zip(*sorted_pairs)
    indices, keys = [ list(tuple) for tuple in  tuples]
    keys

    #Keeping the required content and removing the redundant part
    content = []
    for idx in range(len(indices)):
        if idx != len(indices)-1:
            content.append(text[indices[idx]: indices[idx+1]])
        else:
            content.append(text[indices[idx]: ])

    for i in range(len(indices)):
        parsed_content[keys[i]] = content[i]

    #Displaying the parsed content

    # parsed_content
    data = pd.DataFrame(parsed_content, index=[0])
    print(data)
    return data

#EMAIL
def get_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)[0]


#PHONE NUMBER

def get_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', num) for num in phone_numbers][0]

