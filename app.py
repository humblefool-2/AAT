from flask import Flask, render_template, json, request, redirect, session
import os, uuid
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app=Flask(__name__)
mysql = MySQL()
 
# Default Setting
pageLimit=2
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'kalicharan123'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['UPLOAD_FOLDER']='static/Uploads'
mysql.init_app(app)

app.secret_key = 'why would I tell you my secret key?'

@app.route("/") #home page direct
def main():
	return render_template('index.html')


@app.route('/showSignUp') #signup page direct
def showSignup():
	return render_template('signup.html')


@app.route('/signUp',methods=['POST','GET']) #send entered details to database
def signUp():
     try:
	# read the posted values from the UI
	_name=request.form['inputName'] 
	_email=request.form['inputEmail'] 
	_password=request.form['inputPassword'] 
	# validate the received values
    	if _name and _email and _password:
		conn=mysql.connect() #MySQL connection
		cursor=conn.cursor() #cursor to query our stored procedure
		_hashed_password=generate_password_hash(_password) #using salting module to create hashed password
		cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
		#commit the changes and return success message
		data=cursor.fetchall()
		if len(data) is 0:
	            conn.commit()
		    return json.dumps({'message':'User created successfully !'})
		else:
                    return json.dumps({'error':str(data[0])})
        else:
		return json.dumps({'html':'<span>Enter the required fields</span>'})
     except Exception as e:
        return json.dumps({'error':str(e)})
     finally:
        cursor.close() 
        conn.close()


@app.route('/showSignin') #signin page direct
def showSignin():
	 return render_template('signin.html')


@app.route('/validateLogin',methods=['POST','GET']) #method to validate user
def validateLogin():
	try:
	    _username=request.form['inputEmail']
            _password=request.form['inputPassword']
	    # connect to mysql
 	    con=mysql.connect()
	    cursor=con.cursor()
	    cursor.callproc('sp_validateLogin',(_username,))
	    data=cursor.fetchall()
	    if len(data)>0:
		if check_password_hash(str(data[0][3]),_password):
		    session['user']=data[0][0]
		    return redirect('/showDashboard')
		else:
		    return render_template('error.html',error='Wrong Email address or Password.')
	    else:
		return render_template('error.html',error='Wrong Email address or Password.')
	except Exception as e:
	    return render_template('error.html',error=str(e)) 
	finally:
	    cursor.close()
	    con.close()

@app.route('/userHome') #welcome page direct
def userHome():
	if session.get('user'): #allow only signed user to access 
   	     return render_template('userHome.html')
	else:
	     return render_template('error.html',error='Unauthorized Access')


@app.route('/logout') #logout from signed account
def logout():
	session.pop('user',None)
	return redirect('/')


@app.route('/showAddWish') #wish page direct
def showAddWish():
	return render_template('addWish.html')


@app.route('/addWish',methods=['POST','GET']) #method to add wish
def addWish():
	try:
		if session.get('user'):
		    _title = request.form['inputTitle']
		    _description = request.form['inputDescription']
		    _user = session.get('user')
		    
	 	    if request.form.get('filePath') is None:
	 	    	_filePath=''
	 	    else:
	 	    	_filePath=request.form.get('filePath')
	 	    
	 	    if request.form.get('private') is None:
	 	    	_private=0
	 	    else:
	 	    	_private=1
	 	    	
	 	    if request.form.get('done') is None:
	 	    	_done=0
	 	    else:
	 	    	_done=1
	 	    	
		    conn = mysql.connect()
		    cursor = conn.cursor()
		    cursor.callproc('sp_addWish',(_title,_description,_user,_filePath,_private,_done))
		    data = cursor.fetchall()
	 
		    if len(data) is 0:
		        conn.commit()
		        return redirect('/userHome')
		    else:
		        return render_template('error.html',error = 'An error occurred!')
	 
		else:
		    return render_template('error.html',error = 'Unauthorized Access')
    	except Exception as e:
        	return render_template('error.html',error = str(e))
    	finally:
		cursor.close()
		conn.close()


@app.route('/getWish',methods=['POST','GET']) #retrieving wish
def getWish():
	try:
		if session.get('user'):
		    _user=session.get('user')
		    _limit=pageLimit
		    _offset=request.form['offset']
		    _total_records=0
		    # Connect to MySQL and fetch data
		    con=mysql.connect()
		    cursor=con.cursor()
    	  	    cursor.callproc('sp_GetWishByUSer',(_user,_limit,_offset,_total_records))
		    wishes=cursor.fetchall()
		    cursor.close()
		    cursor=con.cursor()
		    #cursor to select the returned out parameter
		    cursor.execute('SELECT @_sp_GetWishByUser_3');
		    outParam=cursor.fetchall()
		    response=[]
		    wishes_dict=[]
		    #adding all wishes to a dictionary and finally sending it
		    for wish in wishes:
			wish_dict={
				'Id':wish[0],
				'Title':wish[1],
				'Description':wish[2],
				'Date':wish[4]}
			wishes_dict.append(wish_dict)
			#print wishes_dict
		    response.append(wishes_dict)
		    response.append({'total':outParam[0][0]})
		    
		    return json.dumps(response)
		else:
		    return render_template('error.html',error='Unauthorized Access')

	except Exception as e:
		    return render_template('error.html',error=str(e))


@app.route('/getWishById',methods=['POST','GET']) #used to populate the wishes in popup
def getWishById():
	try:
	     if session.get('user'):
	     	_id=request.form['id']
	     	_user=session.get('user')
	     	
	     	conn=mysql.connect()
	     	cursor=conn.cursor()
	     	cursor.callproc('sp_GetWishById',(_id,_user))
	     	result=cursor.fetchall()
	     	
	     	wish=[]
	     	wish.append({'Id':result[0][0],'Title':result[0][1],'Description':result[0][2],'FilePath':result[0][3],'Private':result[0][4],'Done':result[0][5]})
	     	return json.dumps(wish)
	     else:
		    return render_template('error.html',error='Unauthorized Access')

	except Exception as e:
		    return render_template('error.html',error=str(e))
		    
		    
@app.route('/updateWish',methods=['POST','GET'])  #used to update the wish in database
def updateWish():
	try:
	     if session.get('user'):
	     	_user=session.get('user')
	     	_title=request.form['title']
	     	_description=request.form['description']
	     	_wish_id=request.form['id']
	     	_filePath=request.form['filePath']
	     	_isPrivate=request.form['isPrivate']
	     	_isDone=request.form['isDone']
	     	
	     	
	     	conn=mysql.connect()
	     	cursor=conn.cursor()
	     	cursor.callproc('sp_updateWish',(_title,_description,_wish_id,_user,_filePath,_isPrivate,_isDone))
	     	data=cursor.fetchall()
	     	
	     	if len(data) is 0:
	     		conn.commit()
	     		return json.dumps({'status':'OK'})
	     	else:
	     		return json.dumps({'status':'ERROR'})
	  	
	except Exception as e:
		return json.dumps({'status':'Unauthorized access'})
	finally:
		cursor.close()
		conn.close()     			    
	     	
	     
@app.route('/deleteWish',methods=['POST','GET']) #delete wish from database
def deleteWish():
    try:
    	if session.get('user'):
    	    _id=request.form['id']
    	    _user=session.get('user')
    	    
    	    conn=mysql.connect()
    	    cursor=conn.cursor()
    	    cursor.callproc('sp_deleteWish',(_id,_user))
    	    result=cursor.fetchall()
    	    
    	    if len(result) is 0:
    	    	conn.commit()	  
    	    	return json.dumps({'status':'OK'})
    	    else:
    	    	return json.dumps({'status':'An error occured'})
    	else:
    	 	return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return json.dumps({'status':str(e)})
    finally:
        cursor.close()
        conn.close()    
        
        
@app.route('/upload',methods=['GET','POST']) #file upload handler code
def upload():
        if request.method=='POST':   
        	file=request.files['file'] 	
        	extension=os.path.splitext(file.filename)[1]
        	f_name=str(uuid.uuid4())+extension
	     	file.save(os.path.join(app.config['UPLOAD_FOLDER'],f_name))
	     	return json.dumps({'filename':f_name})
	     	
	     	
@app.route('/showDashboard') #directs to dashboard
def showDashboard():
	return render_template('dashboard.html')	
	
	
@app.route('/getAllWishes',methods=['GET','POST']) #fetches all wishes from table which are not private
def getAllWishes():
	try:
	     if session.get('user'):
	     	_user=session.get('user')
	     	conn=mysql.connect()
	     	cursor=conn.cursor()
	     	cursor.callproc('sp_GetAllWishes',(_user,))
	     	result=cursor.fetchall()
	     	#print ('yes')
	     	wishes_dict=[]
	     	for wish in result:
	     	    wish_dict={
	     	    	       'Id':wish[0],
	     	    	       'Title':wish[1],
	     	    	       'Description':wish[2],
	     	    	       'FilePath':wish[3],
	     	    	       'Like':wish[4],
	     	    	       'HasLiked':wish[5]}
	     	    wishes_dict.append(wish_dict)
	     	    #print ('yes')
	     	    #print(wish_dict)
	     	#print (wishes_dict)
	     	#print ('yes')
	     	return json.dumps(wishes_dict)	
	     
	     else:
	     	return render_template('error.html',error = 'Unauthorized Access')
    	except Exception as e:
        	return json.dumps({'status':str(e)})
    	finally:
		cursor.close()
		conn.close()  
		
		
@app.route('/addUpdateLike',methods=['POST','GET']) #method to call AddUpdateLikes procedure for making changes in database
def addUpdateLike():
    try:
        if session.get('user'):
            _wishId = request.form['wish']
            _like = request.form['like']
            _user = session.get('user')
            
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_AddUpdateLikes',(_wishId,_user,_like))
            data = cursor.fetchall()
 
            if len(data) is 0:
                conn.commit()
                cursor.close()
                conn.close()
                conn=mysql.connect()
                cursor=conn.cursor()
                cursor.callproc('sp_getLikeStatus',(_wishId,_user))
                result=cursor.fetchall()
                return json.dumps({'status':'OK','total':result[0][0],'likeStatus':result[0][1]})
            else:
                return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()
       	
	     	

if __name__=="__main__":
	app.debug=True
	app.run()
