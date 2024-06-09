import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
import argparse


def is_shorten_link(token, link):
    params = {
        'access_token': token,
        'v': '5.236',
        'url': link
    }
    url = 'https://api.vk.ru/method/utils.checkLink'
    response = requests.get(url, params=params)
    response.raise_for_status()
    api_data = response.json()
    if api_data.get('response'):
        if link == api_data.get('response').get('link'):
            return '', False
        else:
            return '', True
    if api_data.get('error'):
        return api_data.get('error').get('error_msg'), True


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

    api_data = response.json()
    if api_data.get('response').get('stats'):
        return '', api_data.get('response').get('stats')[0].get('views')
    elif api_data.get('error'):
        return api_data.get('error').get('error_msg'), 0


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

    api_data = response.json()
    if api_data.get('response'):
        return '', api_data.get('response').get('short_url')
    elif api_data.get('error'):
        return api_data.get('error').get('error_msg'), ''


def main():
    load_dotenv()
    service_token = os.environ['VK_SERVICE_TOKEN']

    parser = argparse.ArgumentParser()
    parser.add_argument("link")
    args = parser.parse_args()
    link = args.link

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
    except TypeError as e:
        print(f'Error: {e}')
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
