import sqlite3

from flask import Flask , render_template, redirect , request , session
#flaskのflask,render_template...sessionを使用します宣言
app = Flask(__name__)

app.secret_key = "mkaiaikaigkaihiayrea"

@app.route("/")
def top():
    return redirect("/login")


@app.route("/test")
def test():
    name = "flask"
    return render_template("test.html",name = name)

@app.route("/greet/<text>")
def hello(text):
    return text + "さん、こんにちは"

@app.route("/favorite/<text>")
def greet(text):
    return text + "いいね！！"

@app.errorhandler(404)
def notfound(code):
    return "404ペーーーーーーージ"


#データベースの接続
@app.route("/dbtest")
def dbtest():
    #データベースに接続
    conn = sqlite3.connect('flask.db')
    #どこのデータを抜くかカーソルを充てる。カーソル→目印
    c = conn.cursor()
    #ecebute:実行する
    c.execute("select name,adress from users where id = 1")
    # fetchone:フェッチ：実査に取得する
    user_info = c.fetchone()
    # データベース接続終了
    c.close()

    
    print(user_info)
    return render_template("dbtest.html", user_info = user_info)

#データベースを追加
@app.route("/add")
def add():
    return render_template("add.html")

#データを追加するボタンの処理
@app.route("/add", methods={"POST"})
def add_post():
    if "user_id" in session:
        task = request.form.get("task")
        conn = sqlite3.connect("flask.db")
        c = conn.cursor()
        c.execute()
        conn.commit()
        c.close()
        return redirect("/list")
    else:
        return redirect("/login")

@app.route("/list")
def task_list():
    if "user_id" in session:
        conn = sqlite3.connect("flask.db")
        c = conn.cursor()
        c.execute("select id ,task from task ")
        task_list = []
        for row in c.fetchall():
        task_list.append({"id":row[0], "task":row[1]})
        c.close()
        return render_template("task_list.html" , task_list = task_list)
    else:
        return redirect("/login")

@app.route("/del/<int:id>")
def del_task(id):
    if "user_id" in session:
        conn = sqlite3.connect('flask.db')
        c = conn.cursor()
        c.execute("delete from task where id =?",(id,))
        conn.commit()
        conn.close()
        return redirect("/list")
    else:
        return redirect("/login")


@app.route("/edit/<int:id>")
def edit(id):
    if "user_id" in session:
        conn = sqlite3.connect('flask.db')
        c = conn.cursor()
        c.execute("select task from task where id = ?",(id,))
        task = c.fetchone()
        conn.close()
        task = task[0]
        item = {"id":id,"task":task}
        return render_template("edit.html",task = item)
    else:
        return redirect("/login")


@app.route("/edit" , methods = ["POST"])
def update_task():
    if "user_id" in session:
        item_id = request.form.get("task_id")
        item_id = int(item_id)
        task = request.form.get("task")
        conn = sqlite3.connect('flask.db')
        c = conn.cursor()
        c.execute("update task set task = ? where id = ?",(task , item_id))
        conn.commit()
        conn.close()
        return redirect("/list")
    else:
        return redirect("/login")

@app.route("/regist", methods=["GET"])
def regist_get():
    return render_template("regist.html")

@app.route("/regist",methods=["POST"])
def regist_post():
    name = request.form.get("name")
    password = request.form.get("password")
    conn = sqlite3.connect('flask.db')
    c = conn.cursor()
    c.execute("insert into user values(null,?,?)",(name,password))
    conn.commit()
    conn.close()
    print("--------------------------------------")
    return redirect("/login")


@app.route("/login",methods = ["GET"])
def login_get():
    return render_template("login.html")



@app.route("/login" , methods = ["POST"])
def login_post():
    name = request.form.get("name")
    password = request.form.get("password")
    conn = sqlite3.connect('flask.db')
    c = conn.cursor()
    c.execute("select id from user where name = ? and password = ?",(name,password))
    user_id = c.fetchone()
    conn.close()
    if user_id is None:
        return redirect("login.html")
    else:
        session["user_id"] = user_id[0]
        return redirect("/list")


#-------------これより下にすると表示されない----------------
if __name__ == "__main__":
    #サーバーを起動するよ
    app.run(debug=True)
    #デバッグモードを有効にするよ

