from flask import render_template

from api import erpApi



def get_StorageProcess(pro_list):
    import pandas as pd
    pro_list = pro_list.split("\r\n")
    req_body = {"type":1}
    data = erpApi.storage_getlist.getStorageProcess(req_body)
    data1 = data.text
    data1 = eval(data1)["data"]
    df_data = pd.DataFrame()
    for i in data1:
        df = pd.DataFrame(i)
        for j in df.index:
            # storge = df.loc[j, 'ware_house_bak_name']
            # process_sn = df.loc[j, 'process_sn']
            df.loc[j, 'product_list'] = str(df.loc[j, 'product_list'])
        df_data = df_data.append(df)
    # df_data = df_data[df_data["process_sn"].isin(pro_list)]
    df_data = df_data.fillna("")
    a=11
    return df_data



def getlistingData():
    data = erpApi.base_data.get_store_detail({})
    data = eval(data.text)
    data_1 = data.get("data")
    sid_list = []
    for i in data_1:
        sid=i.get("sid")
        sid_list.append(sid)
    sid = str(sid_list).replace("[","").replace("]","").replace(" ","")
    req_body={
        "sid":sid,
        "length":15000
    }
    lis_data = erpApi.sales_getlist.get_listing(req_body)
    lis_data = eval(lis_data.text)
    return lis_data

def getstoreid():
    data = erpApi.base_data.get_store_detail({})
    data = eval(data.text)
    data_1 = data.get("data")
    return data_1