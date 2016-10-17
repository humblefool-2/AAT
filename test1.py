    #print p_name,pkg,score                                                                                                                                                                 
    print ('1')                                                                                                                                                                             
    #t_id=long(0)                                                                                                                                                                           
    #insert_stmt = (                                                                                                                                                                        
     # "INSERT INTO apps (app_name,pkg_name,app_score) "                                                                                                                                    
    # "VALUES (%s, %s, %L)"                                                                                                                                                                 
    #)                                                                                                                                                                                      
    insert_stmt = "INSERT INTO apps (app_id , app_name, pkg_name , app_score) VALUES ('2', 'abcd',  'anbbb' , '0.8')"                                                                       
    data = (p_name,pkg,score)                                                                                                                                                               
    cursor = mysql.get_db().cursor()                                                                                                                                                        
    return cursor                                                                                                                                                                           
    cur = mysql.connection.cursor()                                                                                                                                                         
    cur.execute("SELECT * FROM apps")                                                                                                                                                       
    return cur                                                                                                                                                                              
    #cursor.execute(insert_stmt)                                                                                                                                                            
    return cursor.fetchall                                                                                                                                                                  
    print str(cursor.fetchall)                                                                                                                                                              
                                                                                                                                                                                            
    print ('2')                                                                                                                                                                             
    return json.dumps("no")                                                                                                                                                                 
  except Exception as e:                                                                                                                                                                    
    return e;                                                                                                                                                                               
    return render_template('error.html',error=str(e))                                                                                                                                       
  finally:                                                                                                                                                                                  
    return json.dumps("yes")                                                                                                                                                                
    #cursor.close()                                                                                                                                                                         
    #con.close()                                                                                                                                                                            
                                                                                                                                                                                            
                                                                                                                                                                                            
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