import json
import os


def add_in_buyer_offers_data(buyer_id, offer_id, offer_data):
    data = json.load(open("data/bayer_offer_data.json"))
    data.setdefault(str(buyer_id), []).append({str(offer_id): offer_data})
    with open("data/bayer_offer_data.json", "w") as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)


def add_in_waiting_for_reg(user_id, user_data):
    data = json.load(open("data/waiting_for_reg.json"))
    data[user_id] = user_data
    with open("data/waiting_for_reg.json", "w") as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)


def give_role_and_save_in_db(user_id, role, user_data):
    data = json.load(open("data/user_info.json"))
    data[role][user_id] = user_data
    with open("data/user_info.json", "w") as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)


def get_data_in_waiting(user_id):
    data = json.load(open("data/waiting_for_reg.json"))
    return data[user_id]


def add_user_in_role(user_id, role):
    data = json.load(open("data/user_role_data.json"))
    data[role].append(user_id)
    with open("data/user_role_data.json", "w") as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)


def read_buyer_offers_data():
    data = json.load(open("data/bayer_offer_data.json"))
    return data


def users_list(role):
    "список пользователей по переданной роли"
    data = json.load(open("data/user_role_data.json"))
    return [int(i) for i in data[role]]


def get_date_time() -> str:
    pass


def price_for_manager(buyer_price):
    """
    Прибавляет 25%
    корректна если входное значение больше 10
    """
    for_manager_price = int(buyer_price) * 1.25
    return int(for_manager_price + 0.5)


def del_waiting_data(user_id):
    try:
        data = json.load(open("data/waiting_for_reg.json", "r"))

        if user_id in data:
            del data[user_id]

        with open("data/waiting_for_reg.json", "w") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

        return True

    except Exception as e:
        return e


def show_all_users(role):
    try:
        users_data = []
        json_file = json.load(open("data/user_info.json", "r"))
        for user_id, data in json_file[role].items():
            link_username = "не имеет ссылки на профиль" if data[
                                                                'link_username'] is None else f"@{data['link_username']}"
            user_info = f"id пользователя: {user_id}\nИО: {data['reg_user_name']}\nномер телефона: {data['phone_number']}\nссылка на профиль: {link_username}"
            users_data.append(user_info)
        return users_data
    except Exception as e:
        return False, e


def show_user_info(role, user_id):
    json_file = json.load(open("data/user_info.json", "r"))
    return json_file[role][user_id]


def search_user_role(user_id):
    try:
        user_ids = json.load(open("data/user_role_data.json", "r"))
        for role, user_id_list in user_ids.items():
            for us_id in user_id_list:
                if us_id == user_id:
                    return role
    except:
        return False


def delete_user_in_db(user_id, role):
    try:
        user_ids_role = json.load(open("data/user_role_data.json", "r"))
        user_ids_info = json.load(open("data/user_info.json", "r"))
        user_ids_role[role].remove(user_id)
        with open("data/user_role_data.json", "w") as file_ids_role:
            json.dump(user_ids_role, file_ids_role, indent=2, ensure_ascii=False)
        file_ids_role.close()
        del user_ids_info[role][user_id]
        with open("data/user_info.json", "w") as file_ids_info:
            json.dump(user_ids_info, file_ids_info, indent=2, ensure_ascii=False)
        file_ids_info.close()
    except Exception as e:
        return False, e


def show_all_daily_offers(buyer_id=None):
    daily_offers = json.load(open("data/bayer_offer_data.json"))
    if buyer_id is None:
        return daily_offers
    else:
        try:
            return daily_offers[buyer_id]
        except Exception as e:
            return None


def clear_offer_data():
    import shutil

    # Удаление содержимого каталога
    folder = "buyer_photos"
    shutil.rmtree(folder)
    os.mkdir(folder)
    with open("data/bayer_offer_data.json", "w") as f:
        f.write("{}")


"""
for buyer menu:
/comm_offer - 
/help - информация по командам
/my_offers - предложения от  
for managerVV menu:
/offers - предложения в течении дня 

for admin and managerTS:


"""
