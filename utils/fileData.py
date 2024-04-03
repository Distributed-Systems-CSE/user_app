import json

def getAllFileData():
    # id:file_name type dic
    all_data={
        1:"file name 1",
        2:"file name 2",
        3:"file name 3",
        4:"file name 4",
    }
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
