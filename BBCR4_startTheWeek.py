import scraperwiki, simplejson, re,urllib

url='http://www.bbc.co.uk/programmes/b006r9xr/episodes/player.json'

data=simplejson.load(urllib.urlopen(url))['episodes']

def getProgDetails(pid):
    purl='http://www.bbc.co.uk/programmes/'+pid+'.json'
    details=simplejson.load(urllib.urlopen(purl))
    print details
    p=details['programme']
    #supp=p['supporting_content_items'][0]['content']
    pid=p['pid']
    prog=p['parent']['programme']['title']
    record={'series':prog,'title':p['short_synopsis'],'pid':pid, 'progPid':pid,'meddesc':p['medium_synopsis'],'longdesc':p['long_synopsis']}
    scraperwiki.sqlite.save(["pid"], record)

    for supp in p['supporting_content_items']:
        pid2=pid+'_'+supp['title']
        record={'series':prog,'title':supp['title'],'pid':pid2, 'progPid':pid,'longdesc':supp['content']}
        scraperwiki.sqlite.save(["pid"], record)

done=[]

for d in data:
    p = d['programme']
    if p['pid'] not in done:
        print 'Fetching prog',p['pid'],p
        getProgDetails(p['pid'])
        done.append(p['pid'])    
        print 'Done:',done   
print 'ok...'