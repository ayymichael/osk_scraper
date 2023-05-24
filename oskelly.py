import requests
import json



def oskelly_scrap():

    id_nums = {}
    id_list = []

    i = 8000
    while i <= 16008:
        response = requests.get("https://oskelly.ru/api/v2/publicprofile/followings-page?userId=10&page="+str(i)+"&pageSize=20&query=",).json()##["response"]

        print("Номер страницы:", i)
        file = open("id.txt", "w", encoding="utf-8")
        for user in response["data"]["items"]:        
            id_list.append(user["id"])
            id_nums["ids"] = id_list
            # print(user["id"])
            json.dump(id_nums, file)
        print(len(id_list))
        file.close()

        i+=1

    
    
    
        
    return id_nums



oskelly_scrap()

