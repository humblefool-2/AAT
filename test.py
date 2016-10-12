from flask import Flask, render_template, redirect, request, session, json
from flaskext.mysql import MySQL
app = Flask(__name__)                                                                                                                                                                       
import urllib2, json,  unirest                                                                                                                                                     
from pattern.en import sentiment                                                                                                                                                            
from bs4 import BeautifulSoup as bs                                                                                                                                                         
mysql = MySQL() 
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'kuchbhi123'
app.config['MYSQL_DATABASE_DB'] = 'app_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['UPLOAD_FOLDER']='/Uploads'
mysql.init_app(app)

@app.route('/analysis',methods=['POST','GET'])
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

@app.route('/sp_page',methods=['POST','GET'])
def specific_page(): #fetches all reviews with their author's name  
  try:    
    #app="https://play.google.com"+link                                                                                                                                                        
    #page=urllib2.urlopen(app)                                                                                                                                                                 
    #soup=bs(page)                                                                                                                                                                             
    #author=soup.find_all('div',class_='review-info')                                                                                                                                          
    #review=soup.find_all('div',class_='review-body with-review-wrapper')                                                                                                                      
    #for d,s in zip(author,review):       
     # r=d.find('span',class_='author-name').get_text()                                                                                                                                        
      #t=s.get_text().encode('utf-8')                                                                                                                                                          
      #print r,t        
    # connect to mysql
    con=mysql.connect()
    cursor=con.cursor()
    cursor.execute("SELECT VERSION()")
    ver = cursor.fetchone()
    if ver:
                     
                     return json.dumps('Connection made.')
    else:
                     return json.dumps('Connection not made.')
  except Exception as e:
    return render_template('error.html',error=str(e)) 
  finally:
    cursor.close()
    con.close()                                                                                                                                                                               

@app.route('/category',methods=['POST','GET'])
def category(): #fetches all apps belong to the category 
  link="https://play.google.com/store/search?q=message%20app"                                                                                                                               
  page=urllib2.urlopen(link)                                                                                                                                                                
  soup=bs(page)                                                                                                                                                                             
  links=soup.find_all('div',class_='card no-rationale square-cover apps small')                                                                                                             
  titles=soup.find_all('div',class_='card no-rationale square-cover apps small')                                                                                                            
  for r,s in zip(links,titles):     
    print r.a['href'],s.img['alt']                                                                                                                                
                                                                                                                                                                                            
@app.route("/",methods=['POST','GET'])                                                                                                                                                                             
def main():
   #return json.dumps('Welcome')
    return render_template('index.html')
  
if __name__ == "__main__":
  #app.debug=True
   app.run(host='0.0.0.0',port=5000,debug=True)

