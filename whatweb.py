#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import threading
import urllib2
import random

is_identification = False
g_index = 0
lock = threading.Lock()

def usage():
    print '''
    python whatweb.py 线程数 目标网站
    example:
    python whatweb.py 20 http://www.baidu.com
    python whatweb.py 15 wwww.baidu.com
    '''

def list_file(dir):
    files = os.listdir(dir)
    return  files

def request_url(url='', data=None, header={}):
    page_content = ''
    request = urllib2.Request(url, data, header)

    try:
        response = urllib2.urlopen(request)
        page_content = response.read()
        #print page_content
    except Exception, e:
        pass

    return page_content

def whatweb(target):
    global is_identification
    global g_index
    global cms

    while True:
        if is_identification:
            break

        if g_index > len(cms)-1:
            break

        lock.acquire()
        eachline = cms[g_index]
        g_index = g_index + 1
        lock.release()

        if len(eachline.strip())==0 or eachline.startswith('#'):
            pass
        else:
            #eachline添加strip()防止空行，后面赋值出错
            url, pattern, cmsname = eachline.split('------')
            html = request_url(target+url)
            rate = float(g_index)/float(len(cms))
            ratenum = int(100*rate)
            sys.stdout.write(random.choice('x+') + ' ' + str(ratenum) + '% ' + target+url +  "\r")
            sys.stdout.flush()

            if pattern.upper() in html.upper():
                is_identification = True
                print "[*] 成功识别CMS：%s，匹配的URL：%s，匹配的规则：%s" % (cmsname.strip('\n').strip('\r'), url, pattern)
                break
    #print threading.currentThread().getName(),'exit'
    return


if __name__ == '__main__':

    if len(sys.argv) != 3:
        usage()
        sys.exit()

    threadnum = int(sys.argv[1])
    target_url = sys.argv[2]

    f = open('/mycode/python/knownsec/wsl/whatweb/cms.txt')
    cms = f.readlines()
    threads = []

    if target_url.endswith('/'):
        target_url = target_url[:-1]

    if target_url.startswith('http://') or target_url.startswith('https://'):
        pass
    else:
        target_url = 'http://' + target_url

    for i in range(threadnum):
        t = threading.Thread(target=whatweb, args=(target_url,))
        threads.append(t)

    print '[*] 开启%d线程'  % threadnum

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print "\n[*] All threads exit"


