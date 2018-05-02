import pandas as pd
import numpy as np
import os
import time

# TODO: change mapping file path
mapping = pd.read_excel('C:\\Users\\janney.zhang\\Desktop\\work\\projects\\Nestle\\2018\\store_url_mapping.xlsx')

# Read in all data files and merge together by local/ti_jd/ti_suning/ti_tmall
# TODO: change the file path
file_path = "C:\\Users\\janney.zhang\\Desktop\\work\\projects\\Nestle\\2018\\reviews\\April"
file_list = os.listdir(file_path)
print("There are %d files."%len(file_list))

local = pd.DataFrame()
ti_jd = pd.DataFrame()
ti_tmall = pd.DataFrame()
ti_suning = pd.DataFrame()

for file_name in file_list:
    if 'download' in file_name:
        name = file_name.split('.')[0] + file_name.split('.')[4]
        name= pd.read_csv(os.path.join(file_path,file_name), encoding = 'utf-8')
        local = pd.concat([local, name], ignore_index = True)
    elif 'jd' in file_name.lower():
        name = file_name.split('.')[2] + file_name.split('.')[7]
        name = pd.read_csv(os.path.join(file_path,file_name), encoding = 'utf-8')
        ti_jd = pd.concat([ti_jd, name], ignore_index = True)
    elif 'tmall' in file_name.lower():
        name = file_name.split('.')[2] + file_name.split('.')[7]
        name = pd.read_csv(os.path.join(file_path,file_name), encoding = 'utf-8')
        ti_tmall = pd.concat([ti_tmall, name], ignore_index = True)
    elif 'suning' in file_name.lower():
        name = file_name.split('.')[2] + file_name.split('.')[7]
        name = pd.read_csv(os.path.join(file_path,file_name), encoding = 'utf-8')
        ti_suning = pd.concat([ti_suning, name], ignore_index = True)
ti_jd['Store'] = 'JD'
ti_tmall['Store'] = 'Tmall'
ti_suning['Store'] = 'Suning'
ti_suning['review_id']= np.NaN
ti_suning['user_id']= np.NaN

# ti_colums and local_clm
ti_clm = ['Store','url','rpc', 'product_description',
          'review_id','review_date', 'username', 'review_text', 'review_rating',
          'variants', 'image_url']
local_clm = ['Store',  'url', 'rpc', 'product_description', 'review_id', 'review_date',
 'username', 'review_text', 'review_rating', 'variant_1', 'variant_2']
ti_tmall.rename(columns={'review_image':'image_url','harvest_product_description':'product_description','retailer_product_code':'rpc','user_id':'username'}, inplace=True)
ti_tmall = ti_tmall[ti_clm]

ti_jd.rename(columns={'#comments':'image_url','harvest_product_description':'product_description','retailer_product_code':'rpc','user_id':'username'}, inplace=True)
ti_jd = ti_jd[ti_clm]

ti_suning.rename(columns={'store':'Store','harvest_product_description':'product_description','retailer_product_code':'rpc','user_id':'username'}, inplace=True)
ti_suning = ti_suning[ti_clm]

# Merge ti data together
ti = pd.concat([ti_jd, ti_tmall, ti_suning])

local.rename(columns = {'store':'Store','title':'product_description', 'creation_date':'review_date'}, inplace= True)
local = local[local_clm]

# Get product stage
def get_stage(title):
    stage = title[title.find("段")-1:title.find("段")+1]
    if stage == "阶段":
        stage = title[title.find("段")-2] +"段"

    if stage == '一段':
        return '1段'
    elif stage == '二段':
        return '2段'
    elif stage == '三段':
        return '3段'
    elif stage == '四段':
        return '4段'
    else:
        return stage

# fix review_text
def fix_text(row):
    review_text = str(row["review_text"]).strip()
    review_text = review_text.replace("\\", "")
    review_text = review_text.replace("\n", "")
    review_text = review_text.replace("\t", "")
    review_text = review_text.replace("\r", "")
    review_text = review_text.replace("\\", "")
    review_text = review_text.replace("\"", "")
    review_text = review_text.replace("\'", "")
    review_text = review_text.replace(",", "，")
    review_text = review_text.replace("*", "")
    review_text = review_text.replace("&gt;", "")
    review_text = review_text.replace("&lt;", "")
    review_text = review_text.replace("&hellip;", "")
    review_text = review_text.replace("&ldquo;", "")
    review_text = review_text.replace("&rdquo;", "")
    review_text = review_text.replace("&nbsp;", "")
    review_text = review_text.replace("&sub;", "")
    review_text = review_text.replace("&omega;", "")
    review_text = review_text.replace("&acute;", "")
    review_text = review_text.replace("&cap;", "")
    review_text = review_text.replace("&Sigma;", "")
    review_text = review_text.replace("&yuml;", "")
    review_text = review_text.replace("&zwnj;", "")
    review_text = review_text.replace(";", "；")
    return review_text

#fix username
def fix_name(row):
    review_text = str(row["username"]).strip()
    review_text = review_text.replace("\\", "")
    review_text = review_text.replace("\n", "")
    review_text = review_text.replace("\t", "")
    review_text = review_text.replace("\r", "")
    review_text = review_text.replace("\\", "")
    review_text = review_text.replace("\"", "")
    review_text = review_text.replace("\'", "")
    review_text = review_text.replace(",", "，")
    review_text = review_text.replace("*", "")
    review_text = review_text.replace("&gt;", "")
    review_text = review_text.replace("&lt;", "")
    review_text = review_text.replace("&hellip;", "")
    review_text = review_text.replace("&ldquo;", "")
    review_text = review_text.replace("&rdquo;", "")
    review_text = review_text.replace("&nbsp;", "")
    review_text = review_text.replace("&sub;", "")
    review_text = review_text.replace("&omega;", "")
    review_text = review_text.replace("&acute;", "")
    review_text = review_text.replace("&cap;", "")
    review_text = review_text.replace("&Sigma;", "")
    review_text = review_text.replace("&yuml;", "")
    review_text = review_text.replace("&zwnj;", "")
    review_text = review_text.replace(";", "；")
    return review_text

def review_text_length(row):
    review_text = str(row["review_text"]).strip()
    return len(review_text)

# concat local and ti JD&Tmall data and deduplicate in the meantime
concat = pd.concat([ti[ti['Store'] != 'Suning'],local]).drop_duplicates(subset = ['review_id'],keep = 'first')

all_data = pd.concat([concat,  ti[ti['Store'] == 'Suning']])

# Mapping with Sub_store
mapping['rpc'] = mapping['rpc'].astype(str)
all_data['rpc'] = all_data['rpc'].astype(str)
all_data_merge = pd.merge(all_data, mapping, on = ['rpc'])
all_data_merge['Stage'] = all_data_merge['product_description'].map(get_stage)


# colums header for output (finally)
clms = ['Store','Sub_store','Store_url','product_description','Brand','Stage','rpc','review_id','username',
'review_rating','variant_1','variant_2','url','review_date','Month','review_text','image_url']

all_data_merge.rename(columns = {'Store_x':'Store', 'url_x':'url'}, inplace=True)
#删除其中的'系统默认好评', '此用户未填写评价内容'
all_data_merge= all_data_merge[True - all_data_merge['review_text'].str.contains('系统默认好评')]
all_data_merge= all_data_merge[True - all_data_merge['review_text'].str.contains('此用户')]
all_data_merge= all_data_merge[True - all_data_merge['review_text'].str.contains('都是系统自动好评')]
# fix review_text and username
all_data_merge['review_text'] = all_data_merge.apply(fix_text,axis=1)
all_data_merge['username'] = all_data_merge.apply(fix_name,axis=1)
all_data_merge['review_length'] = all_data_merge.apply(review_text_length, axis = 1)
# TODO: change month
all_data_merge['Month'] = 'April'
# TODO: change length
length = 250
all_data_merge = all_data_merge[all_data_merge['review_length'] < 250]
all_data_out = all_data_merge[clms]
print(all_data_out.groupby('Store').size())

# TODO: change file name
all_data_out.to_csv("C:\\Users\\janney.zhang\\Desktop\\work\\projects\\Nestle\\2018\\reviews\\nestle_April.csv", index = False, encoding = 'utf-8')
