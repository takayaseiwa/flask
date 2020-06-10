from flask import Flask , render_template
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
    c.execute("select name, adress from users where id = 1")
    # fitchone:フェッチ：実査に取得する
    user_info = c.fetchone(）
    # データベース接続終了
    c.close()

    
    print(user_info)
    return render_template("dbtest.html", user_info = user_info)





#-------------これより下にすると表示されない----------------
if __name__ == "__main__":
    #サーバーを起動するよ
    app.run(debug=True)
    #デバッグモードを有効にするよ

