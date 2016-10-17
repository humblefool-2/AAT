from flask import Flask, render_template, redirect, request, session, json                                                                                                                   
from flaskext.mysql import MySQL 
import MySQLdb
app = Flask(__name__)                                                                                                                                                                       
import urllib2, json, unirest, re                                                                                                                                                           
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
def analysis(review):  #returns sentiment analysis score of a review by fetching the mashape API                                                                                                    
                                                                                                                                                                                            
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
    link="/store/apps/details?id=com.mxtech.videoplayer.ad"                                                                                                                                 
    a=re.search(r'\=(.*)',link,re.M|re.I)                                                                                                                                                   
    p_pkg=a.group(1)   #stores the unique package name of app                                                                                                                                                                 
    app="https://play.google.com"+link                                                                                                                                                      
                                                                                                                                                                                            
    page=urllib2.urlopen(app)                                                                                                                                                               
                                                                                                                                                                                            
    soup=bs(page)                                                                                                                                                                           
    p_name=soup.find('div',class_='id-app-title').get_text().encode('utf-8')  #stores app name that can be searched directly                                                                                                            
    author=soup.find_all('div',class_='review-info')  #fetches the reviewrs' names                                                                                                                                      
                                                                                                                                                                                            
    review=soup.find_all('div',class_='review-body with-review-wrapper')  #fetches their corresponding reviews                                                                                                                  
    cnt=0                                                                                                                                                                                   
    p_score=0                                                                                                                                                                             
    for s in review:  #iterate over all reviews and calculate their individual score                                                                                                                                                                     
      t=s.get_text().encode('utf-8')                                                                                                                                                        
      cnt+=1                                                                                                                                                                                
      p_score+=analysis(s)                                                                                                                                                                
    p_score/=cnt                                                                                                                                                                          
    # connect to mysql database                                                                                                                                                                      
    con = MySQLdb.connect( host="localhost", user="root", passwd="kuchbhi123", db="app_db")                                                                                                                                                                    
    cursor=con.cursor()                                                                                                                                                                                                                                                                                                                                                 
    t_id=long(0)                                                                                                                                                                            
    cursor.callproc('sp_createapp',(p_name,p_pkg,p_score,t_id))                                                                                                                                                                                                                                                                                                      
    cursor.close()                                                                                                                                                                         
    cursor = con.cursor()                                                                                                                                                                   
    cursor.execute('SELECT @_sp_createapp_3');                                                                                                                                                
    outParam = cursor.fetchall()   
    con.commit()
    p_id=long(outParam[0][0])                                                                                                                                                                   
    cursor.close()
    for r in author:
      a_name=r.find('span',class_='author-name').get_text()
      t_id=long(0)
      a_score=long(0)
      cursor=con.cursor()
      cursor.callproc('sp_createuser',(a_name,a_score,t_id))
      cursor.close()
      cursor=con.cursor()
      cursor.execute('SELECT @_sp_createuser_2')
      outParam = cursor.fetchall()   
      con.commit()
      u_id=long(outParam[0][0])
      cursor.close()
      cursor=con.cursor()
      cursor.execute("INSERT INTO user_apps VALUES (%s,%s)",(u_id,p_id))
      con.commit()
      cursor.close()
    return 'OK'
  except MySQLdb.Error, e:
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])  
            return render_template('error.html',error=str('MySQL Error [%d]: %s' % (e.args[0], e.args[1]))  ) 
        except IndexError:
            return render_template('error.html',error=str(e)) 
  except TypeError, e:
        return render_template('error.html',error=str(e))      
  except ValueError, e:
        return render_template('error.html',error=str(e)) 
  finally:                                                                                                                                                                                  
        con.close()
        return 'OK'                                                                                                                                                                                   
                                                                                                                                                                                            
@app.route('/category',methods=['POST','GET'])                                                                                                                                              
def category(): #fetches all apps belong to the category                                                                                                                                    
  link="https://play.google.com/store/search?q=message%20app"                                                                                                                               
  page=urllib2.urlopen(link)                                                                                                                                                                
  soup=bs(page)                                                                                                                                                                             
  links=soup.find_all('div',class_='card no-rationale square-cover apps small') #fetches the links for all listed apps                                                                                                            
  titles=soup.find_all('div',class_='card no-rationale square-cover apps small') #fetches the corresponding names of all apps                                                                                                           
  for r,s in zip(links,titles):                                                                                                                                                             
    print r.a['href'],s.img['alt']
    
@app.route("/",methods=['POST','GET'])                                                                                                                                                                                                                                                                                                                                                  
def main():                                                                                                                                                                                 
   #return json.dumps('Welcome')                                                                                                                                                            
    return render_template('index.html')                                                                                                                                                    
                                                                                                                                                                                            
if __name__ == "__main__":                                                                                                                                                                  
  #app.debug=True                                                                                                                                                                           
   app.run(host='0.0.0.0',port=5000,debug=True)  