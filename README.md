# url-shortener
This script uses VK API to shorten a URL or show link statistics  

# How to start

Python3 should be already installed. Then use pip to install dependencies:

```bash
pip install -r requirements.txt
```

### Environment variables

- VK_SERVICE_TOKEN

.env example:

```
VK_SERVICE_TOKEN=c011g67b5df7470360ab5a34ft462d107da143a9
```

### How to get

1. Sign up [vk.com](https://vk.com)

2. You need a service token for API requests (please see the [documentation](https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/tokens/service-token))

### Run

If you want to shorten url, type it after the 'Please input the link:'

```bash
$ python main.py 
Please input the link: http://example.com/
Short link: https://vk.cc/cxpRt2
```

If you want to see the stats, type a short link:
```bash
$ python main.py
Please input the link: https://vk.cc/cxpRt2
The total number of clicks: 1
```
