
from flask import *

import views
from api.erpApi import run1


app = Flask(__name__,
            static_folder='static',
            template_folder='templates')


@app.route('/')
def hello_world():
    return "Hello world"

@app.route('/index',methods=["POST","GET"])
def index():  # put application's code here
    if request.method=="POST":
        sku_list = request.form.get("sku")
        df = views.get_StorageProcess(sku_list).fillna("")
        data = df.to_dict("records")
        title = df.columns.values
        title = title.tolist()
        return render_template("111111.html", chika=data, biaoti=title)
    a=11
    return render_template("111111.html")


@app.route('/apitest')
def apitest():
    a = run1()
    return a


@app.route('/get_listing')
def get_listing_data():
    data = views.getlistingData()
    return data

@app.route('/get_store_id')
def get_store_ids():
    data = views.getstoreid()
    return data

if __name__ == '__main__':
    app.run(debug=True)


