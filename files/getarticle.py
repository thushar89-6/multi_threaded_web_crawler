import newspaper


def extract(flag,url):
    output=""
    #if flag==1, extract all from crawled.
    if flag==1:
        f=open("files/crawled.txt","r")
        ff=set(x.strip() for x in f)

        for i in ff:
            try:
                #create newspaper Article object of url
                obj = newspaper.Article(i)
                #get its html and parse it
                obj.download()
                obj.parse()
                #if article is detected
                if obj.is_valid_body():
                    output+="Article found at "+i+"\n"
                    #create a name without punctuation and space to get name for article file.
                    pnm = obj.title.strip().replace(" ","_")
                        
                    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
                    for ele in pnm:
                        if ele in punc:
                            pnm = pnm.replace(ele, "")
                    with open("Articles/"+pnm+".txt","w",encoding='utf-8') as v:
                        v.write(obj.text)
                else:
                    output+="Article not detected, skipping...\n"
            except:
                output+="Article not detected, skipping...\n"
    elif flag==0:
        try:
                obj = newspaper.Article(url)
                obj.download()
                obj.parse()
            
                if obj.is_valid_body():
                    output+="Article found at "+url+"\n"
                    pnm = obj.title.strip().replace(" ","_")
                        
                    punc = '''!()-[]{};:|'"\,<>./?@#$%^&*_~'''
                    for ele in pnm:
                        if ele in punc:
                            pnm = pnm.replace(ele, "")
            
                    with open("Articles/"+pnm+".txt","w",encoding='utf-8') as v:
                        v.write(obj.text)
                else:
                    output+="Article not detected, skipping...\n"
        except:
            output+="Article not detected, skipping...\n"
    print("DONE")
    output+="\nOperation completed.\n"
    return output

