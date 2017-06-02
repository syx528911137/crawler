import pymongo
import codecs




mongodb_host = '127.0.0.1'
mongodb_port = 27017
mongo_connection = pymongo.MongoClient(mongodb_host,mongodb_port)
conn = mongo_connection['paper']
db_paper = conn['paper_containletter_a']

f = codecs.open("paper_containletter_a.txt",'w',encoding='utf8')

count = 0
for item in db_paper.find():
    count = count + 1
    if count == 131:
        print "ss"
    print count
    title = item['title']
    title = title.replace('\n',' ')
    # print title
    f.write(title)
    f.write("\r\n")
    f.flush()
f.close()




