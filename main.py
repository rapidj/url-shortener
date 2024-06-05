import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import os


def is_shorten_link(token, link):
    params = {
        'access_token': token,
        'v': '5.236',
        'url': link
    }
    url = 'https://api.vk.ru/method/utils.checkLink'
    response = requests.get(url, params=params)
    response.raise_for_status()
    if response.json().get('response'):
        if link == response.json().get('response').get('link'):
            return '', False
        else:
            return '', True
    if response.json().get('error'):
        return response.json().get('error').get('error_msg'), True


def count_clicks(token, link):
    key = urlparse(link).path.replace('/', '')
    params = {
        'access_token': token,
        'v': '5.236',
        'key': key,
        'url': link,
        'interval': 'forever',
        'extended': 0
    }
    url = 'https://api.vk.ru/method/utils.getLinkStats'
    response = requests.get(url, params=params)
    response.raise_for_status()
    if response.json().get('response'):
        return '', response.json().get('response').get('stats')[0].get('views')
    elif response.json().get('error'):
        return response.json().get('error').get('error_msg'), 0


def shorten_link(token, link):
    params = {
        'access_token': token,
        'v': '5.236',
        'url': link,
        'private': 0
    }
    url = 'https://api.vk.ru/method/utils.getShortLink'
    response = requests.get(url, params=params)
    response.raise_for_status()
    if response.json().get('response'):
        return '', response.json().get('response').get('short_url')
    elif response.json().get('error'):
        return response.json().get('error').get('error_msg'), ''


def main():
    load_dotenv()
    service_token = os.environ['VK_SERVICE_TOKEN']
    link = input('Please input the link: ')
    # url = 'https://dvmn.org/modules/web-api/lesson/vk-short-link/'
    short_link = ''
    clicks_cnt = 0
    try:
        err_msg, is_short_link = is_shorten_link(service_token, link)
        if not err_msg and not is_short_link:
            err_msg, short_link = shorten_link(service_token, link)
        if not err_msg and is_short_link:
            err_msg, clicks_cnt = count_clicks(service_token, link)
    except requests.exceptions.HTTPError as e:
        print(f'Exception error: {e}')
        return

    if err_msg:
        print('Error message: ', err_msg)
        return

    if short_link:
        print('Short link: ', short_link)

    if clicks_cnt:
        print('The total number of clicks: ', clicks_cnt)


if __name__ == '__main__':
    main()
