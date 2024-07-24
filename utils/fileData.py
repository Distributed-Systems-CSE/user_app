import json
import requests

def getAllFileData():
    # id:file_name type dic
    url = "http://127.0.0.1:5001/getChain"
    response = requests.get(url)
    data = response.json()

    all_data= {}
    for item in data['chain']:
        if item.get('data') != "Genesis Block":
            all_data[item.get('data').get('filename')] = item.get('data')
    return all_data

def getSearchFile(file_name):

    all_data={
        1:"file name 1",
        2:"file name 2",
    }

    return all_data

def getFileBlockData(file_id):

    # blockData={
    #     merkel_tree:"",
    #     chunck_map:""
    # }

    merkel_tree=""

    x = '{ "1":"5000", "2":"5001", "3":"5002"}'
    chunk_map = json.loads(x)

    return merkel_tree,chunk_map
