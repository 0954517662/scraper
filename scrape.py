import requests, wikipedia, re, json
from bs4 import BeautifulSoup
from re import match

def youtube(queri):
    req = requests.get('https://www.youtube.com/results?search_query={}'.format(queri))
    soup = BeautifulSoup(req.text, "lxml")
    datas = []
    for ff in soup.find_all('h3'):
        for ff in soup.find_all('a'):
            if '&list=' not in ff['href']:
                if 'watch?v=' in ff['href']:
                    if '\n' not in ff.text:
                        datas.append({'title':ff.text,'url':'https://youtube.com/'+ff['href']})
    result = {
        'status':'OK',
        'result':datas
    }
    return(result)
#=================[ ARSYBAI ]=========[ GIT SCRAPER ]========================================
def github(userid): #Sensitive
    datas = []
    data = {
        'name':None,
        'followers':None,
        'following':None,
        'stars':None,
        'repo':None
    }
    link = 'https://github.com/{}?tab=repositories'.format(userid)
    req = requests.get(link)
    soup = BeautifulSoup(req.content,"lxml")
    for b in soup.find_all('h1'):
        for e in b.findAll('span',{'itemprop':'name'}):
            data['name'] = e.text
    for repo in soup.find_all('div',{'id':'user-repositories-list'}):
        for sito in repo.findAll('h3'):
            for ries in sito.findAll('a'):
                tit = ries.text.replace('\n','')
                tit = tit.replace(' ','')
                datas.append({'title':tit,'url':'http://github.com/{}'.format(ries.get('href'))})
    data['repo'] = datas
    for follow in soup.find_all('a',{'title':'Followers'}):
        for count in follow.findAll('span',{'class':'Counter'}):
            jml = count.text.replace('\n','')
            jml = jml.replace(' ','')
            data['followers'] = jml
    for following in soup.find_all('a',{'title':'Following'}):
        for count1 in following.findAll('span',{'class':'Counter'}):
            jml = count1.text.replace('\n','')
            jml = jml.replace(' ','')
            data['following'] = jml
    for stars in soup.find_all('a',{'title':'Stars'}):
        for count2 in stars.findAll('span',{'class':'Counter'}):
            jml = count2.text.replace('\n','')
            jml = jml.replace(' ','')
            data['stars'] = jml
    return(data)
#==========[ ARSYBAI ]=============[ INSTA USER ]==============================
def instaprofile(un):
    uReq = requests
    bSoup = BeautifulSoup
    website = uReq.get("https://www.instagram.com/{}/".format(str(un)))
    data = bSoup(website.content, "lxml")
    for getInfoInstagram in data.findAll("script", {"type":"text/javascript"})[3]:
        getJsonInstagram = re.search(r'window._sharedData\s*=\s*(\{.+\})\s*;', getInfoInstagram).group(1)
        data = json.loads(getJsonInstagram)
        for instagramProfile in data["entry_data"]["ProfilePage"]:
    	    username = instagramProfile["graphql"]["user"]["username"]
    	    name = instagramProfile["graphql"]["user"]["full_name"]
    	    picture = instagramProfile["graphql"]["user"]["profile_pic_url_hd"]
    	    biography = instagramProfile["graphql"]["user"]["biography"]
    	    followers = instagramProfile["graphql"]["user"]["edge_followed_by"]["count"]
    	    following = instagramProfile["graphql"]["user"]["edge_follow"]["count"]
    	    private = instagramProfile["graphql"]["user"]["is_private"]
    	    media = instagramProfile["graphql"]["user"]["edge_owner_to_timeline_media"]["count"]
    	    result = {
    			"result": {
    				"username": username,
    				"fullname": name,
    				"bio": biography,
    				"followers": followers,
    				"following": following,
    				"media": media,
    				"private": private,
    				"profile_img": picture
    			}
    		}
    	    return(result)
#==========[ ARSYBAI ]======================[ INSTA POSTS ]===============
def instapost(usn):
    datas = []
    link = 'https://instagram.com/{}'.format(usn)
    r = requests.get(link)
    soup = BeautifulSoup(r.content,"lxml")
    for getInfoInstagram in soup.findAll("script", {"type":"text/javascript"})[3]:
        getJsonInstagram = re.search(r'window._sharedData\s*=\s*(\{.+\})\s*;', getInfoInstagram).group(1)
        data = json.loads(getJsonInstagram)
        for insta in data["entry_data"]["ProfilePage"]:
            md = insta["graphql"]["user"]
            md = md["edge_owner_to_timeline_media"]
            for post in md["edges"]:
                url = post["node"]["display_url"]
                video = post["node"]["is_video"]
                datas.append({'url':url,'vid':video})
    return(datas)