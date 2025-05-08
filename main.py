import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from multiprocessing import Pool, current_process
from math import ceil
import logging

def parting(xs, parts):
    part_len = ceil(len(xs)/parts)
    return [xs[part_len*k:part_len*(k+1)] for k in range(parts)]

logging.basicConfig(level=logging.INFO, filename="oskelly.log", filemode="w")

with open("/Users/michael/oskelly/osk_scraper/id.txt") as file:
    ids = list(set(file.read().split(', ')[::-1]))
    print("Список айдишников получен")
    print('Длина списка айдишников - ', len(ids))

url = "https://oskelly.ru/api/v2/publicprofile/following/toggle?userId="

def create_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=4,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def subscriber(lst):
    session = create_session()
    error_ids = []

    for id in lst:
        try:
            user_url = url + id
            response = session.post(user_url, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'Cookie': 'countryCode=RU; tmr_lvid=6c5531150c75d14406703f423ad17538; tmr_lvidTS=1746718987162; _gid=GA1.2.196812280.1746718988; _ym_uid=1746718988261752385; _ym_d=1746718988; domain_sid=BhOLu3bTjpLigVX6phfle%3A1746718987578; _ym_isad=2; mindboxDeviceUUID=949ebff8-bbd3-49c3-ac36-2d8b1e785e12; directCrm-session=%7B%22deviceGuid%22%3A%22949ebff8-bbd3-49c3-ac36-2d8b1e785e12%22%7D; osk=0db4b86e-2f98-4230-ad6f-34999d593120; SESSION=ZjU5MmExNWUtYTE2MC00YjE0LThkN2QtMWUyY2YxNjE4M2Q1; referrer=oskelly.ru; _gat_UA-98397344-1=1; _ga=GA1.1.167338339.1746718988; _ym_visorc=b; _ga_Z98Z4VS6EG=GS2.2.s1746744991$o3$g0$t1746744991$j60$l0$h0; tmr_detect=0%7C1746744993256; gender=men; _ga_0XJSGEJQNK=GS2.1.s1746744990$o3$g1$t1746745001$j49$l0$h0',
                'Connection': 'Keep-Alive'
            })
            json_response = response.json()
            if json_response.get('data') == 'su.reddot.domain.exception.UserNotFoundException':
                logging.info(f"Пользователь не найден: {id}")
            else:
                logging.info(f"{current_process().name}: {json_response.get('message')}")
        except Exception as e:
            logging.error(f"Ошибка при обработке ID {id}: {e}")
            error_ids.append(id)
            with open("errorIds.txt", "a", encoding="utf-8") as f:
                f.write(f"{id}\n")
    print(f"{current_process().name} завершил обработку.")

if __name__ == "__main__":
    process_count = int(input('Количество процессов: '))
    id_list = parting(ids, process_count)
    with Pool(processes=process_count) as p:
        p.map(subscriber, id_list)