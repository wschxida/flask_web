#encoding=utf-8
'''
Created on 2019年05月05日

@author: cedar
'''


import pymysql





conn = pymysql.connect(user='root', passwd='poms@db',
                 host='192.168.1.118', db='mymonitor',charset='utf8mb4')

cur = conn.cursor()
sql= """
        select ad.Article_Detail_ID, ad.Website_No, ad.Article_URL, ad.Article_Title, ad.Article_PubTime
        from article_detail ad
        where ad.Extracted_Time>CURRENT_DATE()
        and ad.Website_No='{}'
        """.format('S16979')
print(sql)

sta=cur.execute(sql)
if sta>=1:
    print('Done')
else:
    print('Failed')

results = cur.fetchall()
for row in results:
    Article_Detail_ID = row[0]
    Website_No = row[0]
    Article_URL = row[0]
    Article_PubTime = row[0]
    print(Article_Detail_ID)


# conn.commit()
cur.close()
conn.close()