import json
from urllib import request

def ltr():
    with request.urlopen('https://newsapi.org/v2/top-headlines?sources=abc-news-au&apiKey=e6ef2cde327f46e3820d0344025b79fc') as response:
        if response.getcode() == 200:
            source = response.read()
            data = json.loads(source.decode('utf-8'))
            val = '00'
            for i in range(1,11):
                # print(data['articles'][int(val)]['title'])
                lo= data['articles']
                # print(lo)
                val = str(int(val) + 1).zfill(len(val))
            out = json.dumps(lo)
            y = json.loads(out)
        else:
            print('An error occurred while attempting to retrieve data from the API.')

    return y


def findltr(id):
    with request.urlopen(
            'https://newsapi.org/v2/top-headlines?sources=abc-news-au&apiKey=e6ef2cde327f46e3820d0344025b79fc') as response:
        if response.getcode() == 200:
            source = response.read()
            data = json.loads(source.decode('utf-8'))
            val = '00'
            for i in range(1, 11):
                # print(data['articles'][int(val)]['description'])
                lo = data['articles'][int(val)]['description']

                my_string = lo
                splitted = my_string.split()

                first = splitted[0]
                if id == first:

                    out = json.dumps(data['articles'][int(val)])
                    jval = json.loads(out)
                    break



                val = str(int(val) + 1).zfill(len(val))


        else:
            print('An error occurred while attempting to retrieve data from the API.')
    return jval



