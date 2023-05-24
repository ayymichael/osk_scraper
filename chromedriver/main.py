from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from multiprocessing import Pool, current_process
import time
from math import ceil


def parting(xs, parts):
    part_len = ceil(len(xs)/parts)
    return [xs[part_len*k:part_len*(k+1)] for k in range(parts)]

errorIds = []

with open("/home/aymichael/studying/python_tst/oskelly/idNew.txt") as file:
        ids = file.read().split(', ')[::-1]
        print("Список айдишников получен")

url = "https://oskelly.ru/"
options = webdriver.ChromeOptions()
options.add_argument("--headless")
# options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
def subscriber(lst):
    print("Инициализация драйвера...")
    driver = webdriver.Chrome(executable_path='./oskelly/chromedriver/chromedriver', 
                                options=options)

    driver.get(url=url)
    time.sleep(3)
    loginBtn = driver.find_element(By.XPATH, "//*[@id='__nuxt']/div/div[3]/span[3]")
    loginBtn.click()
    emailInput = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/form/div[1]/div/input")
    passwordInput = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/form/div[2]/div/input")
    loginBtn1 = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/form/button")

    emailInput.send_keys('login')
    passwordInput.send_keys('password')
    print("Входим в аккаунт...")

    loginBtn1.click()

    time.sleep(5)

    print("Вход произведен, начинаю подписываться...")
    for id in lst:
        try:

            newUrl = 'https://oskelly.ru/profile/' + id
            print(current_process().name, " - ", newUrl)
            prepared_user = driver.get(url=newUrl)
            time.sleep(2)
            subscribeBtn = driver.find_element(By.XPATH, "//*[@id='__nuxt']/div/div[2]/div/div[1]/div/div[2]/div[1]/button")

            if (subscribeBtn.text == 'Подписан (-а)'):
                time.sleep(3)
                continue
            
            subscribeBtn.click() 
            print(current_process().name, " - Done")

            time.sleep(1.5)
    

        except NoSuchElementException as ex:
            errorPage = driver.find_element(By.XPATH, "//*[@id='__nuxt']/div/div[1]")
            errorIds.append(id)
            with open("errorIds.txt", "a", encoding="utf-8") as f:
                        f.write(str(errorIds))
            print("Не удалось подписаться на ", newUrl)
            pass

        # finally: 
        #     driver.close()
        #     driver.quit()
    print("Готово")
if __name__ == '__main__':
    process_count = int(input('Количество процессов: '))
    id_list = parting(ids, process_count)
    p = Pool(processes=process_count)
    p.map(subscriber, id_list)

