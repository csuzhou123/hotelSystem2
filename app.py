# 导入需要的模块，request用于获取表单参数
from flask import Flask, render_template, request
import pymysql
import hashlib

app = Flask(__name__)
con = pymysql.connect(host='localhost', password='123456', database='hotel_system', port=3306, user='root', charset='utf8')
cur = con.cursor()


def select_pwd_from_account(username):
    cur.execute("SELECT password FROM account WHERE username = '%s'" %username)
    return cur.fetchone()

def select_account_from_username(username):
    cur.execute("SELECT * FROM account WHERE username = '%s'" % username)
    return cur.fetchone()

def select_hotel_info():
    cur.execute("SELECT * FROM hotel")
    results = cur.fetchall()
    return results


def select_one_hotel_info(hotel_id):
    cur.execute("SELECT * FROM hotel WHERE hotel_id= '%s'" %hotel_id)
    return cur.fetchone()


def select_house_info(hotel_id):
    cur.execute("SELECT * FROM house WHERE hotel_id= '%s'" % hotel_id)
    return cur.fetchall()


def update_hotel(hotel_id, address, introduction, service, home_type, price, status):
    cur.execute("UPDATE hotel SET hotel_id=%s, address=%s, introduction=%s, service=%s, home_type=%s, price=%s, status=%s  where hotel_id=%s",
                (hotel_id, address, introduction, service, home_type, price, status, hotel_id))


def update_house(house_id, house_type, hotel_id, price, shangquan, stars):
    cur.execute("UPDATE house SET house_id=%s, house_type=%s, hotel_id=%s, price=%s, shangquan=%s, stars=%s where house_id=%s",
                (house_id, house_type, hotel_id, price, shangquan, stars, house_id))


def add_hotel(address, introduction, service, home_type, price, shangquan, stars):
    cur.execute("INSERT INTO hotel(hotel_id, address, introduction, service, home_type, price, shangquan, stars) values(0, %s, %s, %s, %s, %s, %s, %s)",
                (address, introduction, service, home_type, price, shangquan, stars))


def add_account(username, password, name, phone, address, account_type):
    cur.execute(
        "INSERT INTO account(username, password, name, phone, address, account_type) values(%s, %s, %s, %s, %s, %s)",
        (username, password, name, phone, address, account_type))


def add_house(house_type, hotel_id, price, status):
    cur.execute(
        "INSERT INTO house(house_id, house_type, hotel_id, price, status) values(0, %s, %s, %s, %s)",
        (house_type, hotel_id, price, status))


def select_all_hotel_manager():
    cur.execute("SELECT * FROM account")
    return cur.fetchall()


# 跳转到登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("form/login.html")
    else:
        username = request.form['username']
        password = request.form['password']
        # md5加密
        pwd = hashlib.md5(password.encode(encoding='utf-8')).hexdigest()
        if pwd.__eq__(select_pwd_from_account(username)):
            if select_account_from_username(username)[5].__eq__('hotel_manager'):
                results = select_hotel_info()
                return render_template("form/hotel.html", results=results)
            else:
                return render_template("form/systemManger.html")
        else:
            return render_template("form/error.html")


@app.route('/viewhotel/<hotel_id>', methods=['GET', 'POST'])
def viewhotel(hotel_id):
    hotel = select_one_hotel_info(hotel_id)
    return render_template("form/hotelInfo.html", hotel=hotel)


@app.route('/updatehotel', methods=['GET', 'POST'])
def updatehotel():
    if request.method == 'POST':
        update_hotel(request.form['hotel_id'], request.form['address'], request.form['introduction'],
                     request.form['service'], request.form['home_type'], request.form['price'], request.form['status'])
        hotel = select_one_hotel_info(request.form['hotel_id'])
        return render_template("form/hotelInfo.html", hotel=hotel)


@app.route('/viewhouse/<hotel_id>', methods=['GET', 'POST'])
def viewhouse(hotel_id):
    houses = select_house_info(hotel_id)
    return render_template("form/houseInfo.html", houses=houses)


@app.route('/updatehouse', methods=['GET', 'POST'])
def updatehouse():
    update_house(request.form['house_id'], request.form['house_type'], request.form['hotel_id'],
                     request.form['price'], request.form['shangquan'], request.form['stars'])
    houses = select_house_info(request.form['hotel_id'])
    return render_template("form/houseInfo.html", houses=houses)


@app.route('/viewaddhouse', methods=['GET', 'POST'])
def viewaddhouse():
    return render_template("form/newHouse.html")

@app.route('/addhouse', methods=['GET', 'POST'])
def addhouse():
    add_house(request.form['house_type'], request.form['hotel_id'],
                     request.form['price'], request.form['status'],)
    houses = select_house_info(request.form['hotel_id'])
    return render_template("form/houseInfo.html", houses=houses)


@app.route('/viewaddhotel', methods=['GET', 'POST'])
def viewaddhotel():
    return render_template("form/newHotel.html")


@app.route('/addhotel', methods=['GET', 'POST'])
def addhotel():
    add_hotel(request.form['address'], request.form['introduction'],request.form['service'],
              request.form['home_type'], request.form['price'], request.form['shangquan'],
              request.form['stars'])
    results = select_hotel_info()
    return render_template("form/hotel.html", results=results)


@app.route('/viewaddaccount', methods=['GET', 'POST'])
def viewaddaccount():
    return render_template("form/newAccount.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    add_account(request.form['username'], hashlib.md5(request.form['password'].encode(encoding='utf-8')).hexdigest(),
                request.form['name'], request.form['phone'], request.form['address'], 'hotel_manager')
    results = select_all_hotel_manager()
    return render_template("form/hotelManager.html", results=results)


if __name__ == '__main__':
    app.run()
