import requests
import time

def oskelly_scrap(max_retries: int = 4, retry_delay: float = 1.0):
    id_list = []

    for i in range(13, 138):
        url = (
            'https://oskelly.ru/api/v2/publicprofile/followings-page'
            f'?userId=193247&page={i}&pageSize=5250&query='
        )

        for attempt in range(1, max_retries + 1):
            try:
                resp = requests.get(url)
                resp.raise_for_status()  # HTTPError для 4xx/5xx
                data = resp.json()
                break
            except (requests.exceptions.RequestException, ValueError) as e:
                print(f"[Стр. {i}] Ошибка ({e.__class__.__name__}): {e}")
                if attempt < max_retries:
                    print(f" → Попытка {attempt+1}/{max_retries} через {retry_delay}s…")
                    time.sleep(retry_delay)
                else:
                    print(f" → Не удалось получить данные для страницы {i}, пропускаем.")
                    data = None

        if not data:
            continue

        items = data.get('data', {}).get('items', [])
        print(f"[Стр. {i}] Количество словарей: {len(items)}")
        for user in items:
            id_list.append(user.get('id'))


        with open("id.txt", "a", encoding="utf-8") as file:
            file.write(str(id_list))

    print('Ready')


if __name__ == "__main__":
    oskelly_scrap()
