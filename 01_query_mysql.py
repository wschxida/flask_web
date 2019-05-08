#encoding=utf-8
'''
Created on 2019年05月05日

@author: cedar
'''

from flask import Flask
from flask import request
import pymysql
import requests



app = Flask(__name__)

##查询列表
def select_article_detail(website_no,page_no=1):
    conn = pymysql.connect(user='root', passwd='poms@db',
                     host='192.168.1.118', db='mymonitor',charset='utf8mb4')
    cur = conn.cursor()
    if page_no:
        page_no_pre = (int(page_no)-1) * 20
        page_no_post = 20
    else:
        page_no_pre = 0
        page_no_post = 20
    sql= """
        select ad.Article_Detail_ID, ad.Website_No, ad.Article_URL, ad.Article_Title, ad.Article_PubTime
        from article_detail ad
        where ad.Extracted_Time>CURRENT_DATE()
        and ad.Website_No='{}' limit {},{}
        """.format(website_no,page_no_pre,page_no_post)
    print(sql)
    sta=cur.execute(sql)
    if sta>=1:
        print('Done')
    else:
        print('Failed')

    results = cur.fetchall()
    for row in results:
        yield row
    # return results

    # conn.commit()
    cur.close()
    conn.close()


##查询详细
def select_article_content(article_detail_id):
    conn = pymysql.connect(user='root', passwd='poms@db',
                     host='192.168.1.118', db='mymonitor',charset='utf8mb4')
    cur = conn.cursor()
    sql= """
        select ad.Article_Detail_ID, ad.Website_No, ad.Article_URL, ad.Article_Title, ad.Article_PubTime, ac.Article_Abstract, ac.Article_Content
        from article_detail ad, article_content ac 
        where ad.Record_MD5_ID=ac.Article_Record_MD5_ID 
        and ad.Extracted_Time>CURRENT_DATE()
        and ad.article_detail_id={}
        """.format(article_detail_id)
    print(sql)
    sta=cur.execute(sql)
    if sta>=1:
        print('Done')
        results = cur.fetchall()
        # for row in results:
        #     yield row
        return results
    else:
        print('Failed')
        return ""

    # conn.commit()
    cur.close()
    conn.close()


def get_html(url):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "Connection": "keep - alive",
    }
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    text = response.text

    return text



@app.route('/', methods=['GET', 'GET'])
def home():
    return '''
    <br>
    <p><h1><a href="/article_detail">读取mysql文章列表及详情</a></h1></p>
    <br>
    <p><h1><a href="/input_url">实时获取文章详情</a></h1></p>
    '''

@app.route('/article_detail', methods=['GET'])
def article_detail():
    page_no = request.args.get("page_no")
    article_detail = select_article_detail('S16863',page_no)
    # print(article_detail)
    td_html = ''
    row_count = 0

    for row in article_detail:
        row_count += 1
        Article_Detail_ID = row[0]
        Article_Content_URL = '/article_content?Article_Detail_ID=' + str(Article_Detail_ID)
        Website_No = row[1]
        Article_URL = row[2]
        Article_Title = row[3]
        Article_PubTime = row[4]

        td = '''
        <tr>
        <td><a href="{}">{}</a></td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td><a href="{}">原文</a></td>
        </tr>
        
        '''.format(Article_Content_URL,Article_Detail_ID, Website_No, Article_Title, Article_PubTime, Article_URL)
        td_html = td_html + td

    if page_no:
        nextpageno = int(page_no)+1
        nextpage = '/article_detail?page_no=' + str(nextpageno)
        if row_count<20:
            nextpageno = int(page_no)
            nextpage = '/article_detail?page_no=' + str(nextpageno)

        lastpageno = int(page_no) - 1
        if lastpageno==0:
            lastpageno = 1
        lastpage = '/article_detail?page_no=' + str(lastpageno)
    else:
        nextpage = '/article_detail?page_no=2'
        lastpage = '/article_detail?page_no=1'

    html = '''
    <div style="width:1000px;text-align:center;margin:0 auto">
    <h3 style="text-align:center;margin:20 auto">文章列表</h3>
    <table border="1" align="center"  width="1000">
    '''+td_html+'''</table> <br><a href="{}">上一页</a><span>     </span><a href="{}">下一页</a></div>'''.format(lastpage,nextpage)

    return html

@app.route('/article_content', methods=['GET'])
def article_content():

    article_detail_id = request.args.get("Article_Detail_ID")
    if article_detail_id:
        content = select_article_content(article_detail_id)
        if content:
            Article_Title = content[0][3]
            Article_PubTime = content[0][4]
            # Article_Abstract = content[0][5]
            Article_Content = content[0][6]

            return '''<div style="width:1000px;text-align:center;margin:0 auto">
                <br><br>
                <h3>{}</h3>
                <p>{}</p>
                <br>
                {}
                </div>'''.format(Article_Title, Article_PubTime, Article_Content)
        else:
            return "No content."
    else:
        return "No content."


@app.route('/input_url', methods=['GET'])
def input_url():

    return '''
    <form action="/html_result" method="post" align="center">
              <h1 style="width: 50%; height:50px; margin: 50px auto 0 auto; font-size: 2rem;">请输入URL</h1>
			  <textarea  rows="1" cols="120" style="width: 50%; height:50px;margin: 0 auto 10px auto; font-size: 1.5rem;" name="article_url" title="请输入标题"></textarea>
			  <p><button type="submit" style="width: 10%; height:50px; font-size: 1rem;">获取</button></p>
              </form>
    '''

@app.route('/html_result', methods=['POST'])
def html_result():

    article_url = request.form['article_url']
    article_url = article_url.replace('http://', '')
    article_url = article_url.replace('https://', '')
    article_url = "http://" + article_url
    article_html = get_html(article_url)
    return article_html


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)



