import pymongo
from scrapy.conf import settings

connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
db = connection[settings['MONGODB_DB']]
collection = db[settings['MONGODB_COLLECTION_BIGDATA']]
collection_Dup_remove = db['bigdata_dup_remove']

authIds = []

querys = collection.find()
count = 0
for item in querys:
    count = count + 1
    authid = item['authId']
    flag = authIds.__contains__(authid)
    if flag == False :
        authIds.append(authid)
print len(authIds)

for id in authIds:
    items = collection.find({'authId':id})
    length = 0
    save_item = ''
    for item in items:
        tmp_len = len(item)
        if tmp_len > length:
            length = tmp_len
            save_item = item
    collection_Dup_remove.insert(save_item)
    print len(save_item)
