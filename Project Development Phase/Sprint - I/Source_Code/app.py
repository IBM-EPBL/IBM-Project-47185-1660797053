from flask import Flask, render_template , request , redirect , session
import ibm_db


conn_str='<String>'
conn = ibm_db.connect(conn_str,'','')
 

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'ugfcx86r6it7ypn7lv98i6d5'

# @app.route("/db",methods=['GET'])
# def db():
#    sql = "create table query (id integer not null GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),email varchar(500),name varchar(500),query varchar(500),data varchar(50),PRIMARY KEY (id));"
#    sql = "create table users (id integer not null GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),name varchar(500),email varchar(500),password varchar(225),mob varchar(50),PRIMARY KEY (id));"
#    stmt = ibm_db.exec_immediate(conn, sql)
#    return "ok"


@app.route("/",methods = ['GET'])
def index():
    return render_template("login.html")

@app.route("/signin",methods = ['POST'])
def index_signin():
    sql = "select * from users where email='"+request.form["email"]+"'"
    stmt = ibm_db.exec_immediate(conn, sql)
    data = []
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        data.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    if(data):
        if(data[0]["PASSWORD"]==request.form["password"]):
            session["user"]=data[0]["ID"]
            session["name"]=data[0]["NAME"]
            session["email"]=data[0]["EMAIL"]
            return redirect("/user")
        else:
            return redirect("/")
    else:
        return redirect("/")

@app.route("/register",methods = ['GET'])
def index_register():
    return render_template("register.html")

@app.route("/signup",methods = ['POST'])
def index_signup():
    sql = "INSERT INTO users (name , email , password,mob)values('"+request.form["name"]+"','"+request.form["email"]+"','"+request.form["password"]+"','"+request.form["mob"]+"')"
    stmt = ibm_db.exec_immediate(conn, sql)
    return redirect("/")
    



if __name__ == '__main__':
   app.run()