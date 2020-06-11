import sqlite3

from flask import Flask , render_template, redirect , request
#flaskのflask,render_templateを使用します宣言
app = Flask(__name__)

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
    # add.htmlからformのname="task"を取得
    task = request.form.get("task")
    # データベースに接続
    conn = sqlite3.connect("flask.db")
    c = conn.cursor()
    # (task,)のカンマは忘れずにね。タプル型なので
    # ?に(task,)が入るよ
    # insert into はデータを追加
    c.execute("insert into task values(null, ?)", (task,))
    conn.commit()
    c.close()
    return "データを追加できました！"

@app.route("/list")
def task_list():
    conn = sqlite3.connect('flask.db')
    c = conn.cursor()
    c.execute("select id ,task from task ")
    task_list = []
    for row in c.fetchall():
        task_list.append({"id":row[0], "task":row[1]})
    conn.close()
    return render_template("list.html , task_list = task_list")


@app.route("/del/<int:id>")
def del_task(id):
    conn = sqlite3.connect('flask.db')
    c = conn.cursor()
    c.execute("delete from task where id =?",(id,))
    conn.commit()
    conn.close()
    return redirect("/list")



#-------------これより下にすると表示されない----------------
if __name__ == "__main__":
    #サーバーを起動するよ
    app.run(debug=True)
    #デバッグモードを有効にするよ

