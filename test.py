import urllib2, json, requests, unirest 
from pattern.en import sentiment   
from bs4 import BeautifulSoup as bs

def analysis(review):  #used for sentiment analysis of all reviews of a particular app                                                                                                                                                     
  response = unirest.post("https://twinword-sentiment-analysis.p.mashape.com/analyze/",                                                                                                       
  headers={                                                                                                                                                                                 
    "X-Mashape-Key": "I30aaFxZvwmshEZnfICyrLJcwpEjp1e80CPjsnCufIeFbQptxJ",                                                                                                                  
    "Content-Type": "application/x-www-form-urlencoded",                                                                                                                                    
    "Accept": "application/json"                                                                                                                                                            
    },                                                                                                                                                                                        
  params={                                                                                                                                                                                  
      "text": review                                                                                                                                                                          
    }                                                                                                                                                                                         
  )                                                                                                                                                                                           
  return (response.body['score'])   

def specific_page(link): #fetches all reviews with their author's name
  app="https://play.google.com"+link
  page=urllib2.urlopen(app)
  soup=bs(page)
  author=soup.find_all('div',class_='review-info')
  review=soup.find_all('div',class_='review-body with-review-wrapper')
  for d,s in zip(author,review):
    r=d.find('span',class_='author-name').get_text()
    t=s.get_text().encode('utf-8')
    print r,t
    
def category(): #fetches all apps belong to the category
  link="https://play.google.com/store/search?q=message%20app"
  page=urllib2.urlopen(link)
  soup=bs(page)
  links=soup.find_all('div',class_='card no-rationale square-cover apps small')
  titles=soup.find_all('div',class_='card no-rationale square-cover apps small')
  for r,s in zip(links,titles):
    print r.a['href'],s.img['alt']

category()
                                                                                                                                                                                                                                                                                                                                                                                                   
