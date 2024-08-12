from bs4 import BeautifulSoup as bs
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
import os
import re

#crawls all files in uncrawled.txt if texxt is "" adds all obtained links to uncrawled and all uncrawled links to crawled.txt. If not "" checks all crawled urls and adds only links containing texxt to uncrawled. Second argument is no of threads.
def new(texxt,no,itr):
    try:
        #output string which stores all messages and returns it
        output=""
        #create a set
        temp=set()
        output+="\nKeyword: "+texxt+"\n"
        #open files and load contents into sets crawled and uncrawled
        if not os.path.exists("files/crawled.txt"):
            crawled_txt=open("files/crawled.txt", "w+")
        else:
            crawled_txt=open("files/crawled.txt","r+",encoding='utf-8')

        if not os.path.exists("files/uncrawled.txt"):
            uncrawled_txt=open("files/uncrawled.txt","w+")
        else:
            uncrawled_txt=open("files/uncrawled.txt","r+",encoding='utf-8')

        crawled=set(line.strip() for line in crawled_txt)
        uncrawled=set(line.strip() for line in uncrawled_txt)

        #pop one link from uncrawled and get base url.
        link=uncrawled.pop()
        uncrawled.add(link)
        #find pattern starting from https:// and first / 
        link+="/"#if we enter base url itself it needs to have / at end for pattern to detect
        u= re.findall(r"(https://.+?/)",link)
        base_url=u[0]
        output+="Base url: "+base_url+"\n"

        #create a lock object to lock and unlock temp set so that only one thread can acess it at a time.
        lock = threading.Lock()
        def crawl(url,temp):
            user_agent = 'Mozilla/5.0'
            headers = {'User-Agent': user_agent }
            #send http get request and get the html 
            obj=requests.get(url,headers)
            soup = bs(obj.content,'html.parser')
            #get all anchor tag and add content in href to temp with locking to achieve synchronization.
            for i in soup.find_all('a'):
                #add base url to urls which are relative
                link=urljoin(base_url,i.get('href'))
                if (link not in crawled) and (link not in temp):
                    lock.acquire()
                    temp.add(link)
                    lock.release()

        #create thread pool with no threads and submit crawl function with arguments to that many threads at a time. wait for it to complete.
        

        for i in range(itr):
            executor = ThreadPoolExecutor(max_workers=no)
            for url in uncrawled:
                executor.submit(crawl,url, temp)
            executor.shutdown(wait=True)
            #add content of uncrawled to crawled set, set uncrawled as temp and empty temp.
            n=len(uncrawled)
            crawled.update(uncrawled)
            uncrawled=temp
            temp=set()
            output+=str(len(uncrawled))+" links obtained from "+str(n)+" sites.\n"
            output+="Total links crawled: "+str(len(crawled))+"\n"
        #update content of sets to their respective txt files.
        for i in crawled:
            if i!=None:
                crawled_txt.write(i+'\n')
        if texxt=="":
            for i in uncrawled:
                if i!=None:
                    uncrawled_txt.write(i+'\n')
        else:
            c=0
            for i in uncrawled:
                if i!=None and texxt in i:
                    uncrawled_txt.write(i+'\n')
                    c+=1
            output+=str(c)+" links found with "+texxt+" in it."
                
        uncrawled_txt.close()
        crawled_txt.close()
    except:
        return "\nError occured.\n"
    output+="\nOperation completed.\n"
    return output
    