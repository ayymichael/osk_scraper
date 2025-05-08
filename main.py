import requests
from multiprocessing import Pool, current_process
from math import ceil
import logging
import time

def parting(xs, parts):
    part_len = ceil(len(xs)/parts)
    return [xs[part_len*k:part_len*(k+1)] for k in range(parts)]

errorIds = []

with open("/home/aymichael/studying/python_tst/oskelly/myIds.txt") as file:
        ids = list(set(file.read().split(', ')[::-1]))
        print("Список айдишников получен")
        print('Длина списка айдишников - ', len(ids))

url = "https://oskelly.ru/api/v2/publicprofile/following/toggle?userId="
logging.basicConfig(level=logging.INFO, filename="oskelly.log",filemode="w")

def subscriber(lst):
    for id in lst:
        try:
            userUrl = url + id
            # print('Пользователь - ', userUrl)
            response = requests.post(userUrl, headers={
                 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                 'Cookie': 'countryCode=RU; tmr_lvid=6c5531150c75d14406703f423ad17538; tmr_lvidTS=1746718987162; _gid=GA1.2.196812280.1746718988; _ym_uid=1746718988261752385; _ym_d=1746718988; domain_sid=BhOLu3bTjpLigVX6phfle%3A1746718987578; _ym_isad=2; _ym_visorc=b; mindboxDeviceUUID=949ebff8-bbd3-49c3-ac36-2d8b1e785e12; directCrm-session=%7B%22deviceGuid%22%3A%22949ebff8-bbd3-49c3-ac36-2d8b1e785e12%22%7D; osk=0db4b86e-2f98-4230-ad6f-34999d593120; SESSION=ZjU5MmExNWUtYTE2MC00YjE0LThkN2QtMWUyY2YxNjE4M2Q1; gender=men; referrer=oskelly.ru; _gat_UA-98397344-1=1; _ga_0XJSGEJQNK=GS2.1.s1746718987$o1$g1$t1746720119$j59$l0$h0; _ga=GA1.1.167338339.1746718988; _ga_Z98Z4VS6EG=GS2.2.s1746718987$o1$g1$t1746720119$j60$l0$h0; tmr_detect=0%7C1746720122247',
                 'Connection': 'Keep-Alive'
                 })
            if (response.json()['data'] == 'su.reddot.domain.exception.UserNotFoundException'):
                logging.info(msg={'Пользователь не найден': id})
                pass
            # while (response.json()['message'] == 'Подписка отменена'):
            #     time.sleep(1)
            #     response = requests.post(userUrl, headers={
            #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            #     'Cookie': '_ym_uid=1677051194400616439; tmr_lvid=bb25bdeb8f7d1089541206b60939e4a4; tmr_lvidTS=1677051194160; mindboxDeviceUUID=8c30e47e-b16c-4db5-8a9d-fb11bbc74316; directCrm-session=%7B%22deviceGuid%22%3A%228c30e47e-b16c-4db5-8a9d-fb11bbc74316%22%7D; osk=7834fdd2-11bf-460b-85c3-77718eeb3a28; _ym_d=1694465798; _gid=GA1.2.56683692.1695898857; _ym_isad=1; _ym_visorc=w; SESSION=MjY2ODk0NzktNTQzNy00NjZkLTliOWUtMDRkNjE5Yzg4NzAx; usedesk-widget__login-user-data={%22email%22:%22m_panferov@inbox.ru%22}; gender=men; _gat_UA-98397344-1=1; _ga_0XJSGEJQNK=GS1.1.1695898856.134.1.1695899588.26.0.0; _ga=GA1.2.1106989166.1677051194; _ga_Z98Z4VS6EG=GS1.2.1695898857.6.1.1695899588.27.0.0',
            #     'Connection': 'Keep-Alive'
            #     })
            #     logging.info('Уже подписаны')
            logging.info(response.json()['message'])
            logging.info(msg={current_process().name: 'done'})

        except BaseException as e:
            logging.error(e, id)
            errorIds.append(id)
            with open("errorIds.txt", "a", encoding="utf-8") as f:
                        f.write(str(errorIds))
            pass
    print("Готово")
if __name__ == '__main__':
    process_count = int(input('Количество процессов: '))
    id_list = parting(ids, process_count)
    p = Pool(processes=process_count)
    p.map(subscriber, id_list)

