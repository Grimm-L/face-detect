import requests
import json
import redis
import hashlib

r = redis.Redis(host='localhost', port=6379, db=0)


def access_db_to_json(user_name):
    resp = requests.get("https://444657233z.zicp.fun/wx/order/getWillUsed/?username=" + str(user_name))
    # resp = requests.get("http://127.0.0.1:8000/detect/menu")
    if len(resp.text) == 0 or resp.text == "[]":
        raise Exception("The Response of the DB is empty.")
    # print(resp.text)
    r.set("active_menu", resp.text)


def parse_menu_info_from_redis():
    menu_source_string = r.get("active_menu")
    menu_data = json.loads(menu_source_string)
    menu_res = {"menus": []}
    menu_cnt = 0
    menu_price = 0
    menu_res["user_name"] = menu_data[0]["username"]
    menu_res["rem"] = menu_data[0]["money"]
    menu_res["userId"] = menu_data[0]["userId"]
    for m in menu_data:
        if m["status"] == "已支付":
            menu_res["menus"].extend(m["orderDetails"])
            menu_cnt += m["num"]
            menu_price += m["price"]

    menu_res["total_cnt"] = menu_cnt
    menu_res["total_price"] = menu_price
    return menu_res, hashlib.md5(menu_source_string).hexdigest()


if __name__ == '__main__':
    access_db_to_json("5135")
    print(json.loads(r.get("active_menu")))
