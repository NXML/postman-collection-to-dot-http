import json
import os
import unicodedata
import re
import sys


print(sys.argv)


POSTMAN_COLLECTION_PATH = str(sys.argv[1]).replace('\u200b', '')
print(POSTMAN_COLLECTION_PATH)
OUTPUT_FOLDER = "./output/"

POSTMAN_COLLECTION = None


f = open(POSTMAN_COLLECTION_PATH,encoding='utf-8')
text = f.read().replace('\u200b', '')
POSTMAN_COLLECTION = json.loads(text)
f.close()

def sanitize(value, allow_unicode=True):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')



def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)




def parsePostmanCollection(collection,basePath):
    if 'item' in collection:
        for item in collection['item']:
            itemName = sanitize(item['name'])
            # C'est un fichier de requète
            if "event" in item:
                request = item["request"]
                verb = request["method"]
                url = request['url']['raw']
                headers = request["header"]
                
                httpFile = open(f'{basePath}{itemName}.http','w')
                httpFile.write(f'### {item["name"]}\n')
                httpFile.write(f'{verb} {url}\n')
                for header in headers:
                    httpFile.write(header['key']+": "+header['value']+"\n")
                if  verb in ['POST','PUT']:
                    rawBody = request['body']['raw']
                    httpFile.write('\n'+rawBody.replace('\r',''))
                httpFile.close()
                pass
            # C'est un folder on le Créé
            else:
                print(itemName)
                mkdir(basePath+itemName)
                
            parsePostmanCollection(item,f'{basePath}{itemName}/')

            

    return []









parsePostmanCollection(POSTMAN_COLLECTION,OUTPUT_FOLDER)
