import requests
import json
import time
from urllib.request import urlopen
from datetime import datetime


# 날짜(YYYYMMDD) 출력 함수
# 오늘의 날짜를 YYYYMMDD 형태로 반환한다.
def base_date():
    return datetime.today().strftime('%Y%m%d')


# 시각(HH00) 출력 함수
# 기상청 단기예보 발표 시각 중 현재 시각과 비교하여 최신의 시각을 반환한다.
def base_time():
    # 현재 시각은 정수로, 기상청 단기예보 발표 시각은 리스트로 각각 변수에 저장한다.
    n = int(str(datetime.now().hour))
    announcement = [2, 5, 8, 11, 14, 17, 20, 23]

    # 기상청 단기예보 발표 시각 중 현재 시각과 가까운 값을 구한다.
    announcement.sort()
    N = min(announcement, key=lambda var: abs(var - n))

    # 값이 현재 시각보다 크면 그 이전의 시각을 구한다.
    if N <= n:
        x = N
    else:
        if N - 3 < 0:
            x = announcement[-1]
        else:
            x = N - 3

    # 변수 x의 값을 HH00 형태로 치환한다.
    if x >= 10:
        return f'{x}00'
    else:
        return f'0{x}00'


# [A시 B구 C동] -> [기상청 격자정보 (nx, ny)] 치환 함수
# city, mdl, leaf 변수 선언이 선행되어야 (nx, ny) 값을 반환한다.
def get_nxy():
    global nx, ny

    with urlopen(f'https://www.kma.go.kr/DFSROOT/POINT/DATA/top.json.txt') as resp:
        response1 = json.load(resp)
        top_list = eval(str(response1))

    city_code = [str(top_list[_].get('code')) for _ in range(len(top_list)) if city in top_list[_].values()][0]

    with urlopen(f'https://www.kma.go.kr/DFSROOT/POINT/DATA/mdl.{str(city_code)}.json.txt') as resp:
        response2 = json.load(resp)
        mdl_list = eval(str(response2))

    mdl_code = [str(mdl_list[_].get('code')) for _ in range(len(mdl_list)) if mdl in mdl_list[_].values()][0]

    with urlopen(f'https://www.kma.go.kr/DFSROOT/POINT/DATA/leaf.{str(mdl_code)}.json.txt') as resp:
        response3 = json.load(resp)
        leaf_list = eval(str(response3))

    for _ in range(len(leaf_list)):
        if leaf in leaf_list[_].values():
            nx = str(leaf_list[_].get('x'))
            ny = str(leaf_list[_].get('y'))
            break

    return nx, ny


# 기상청 단기예보 출력 함수
# nx, ny 변수 선언이 선행되어야 json 데이터를 반환한다.
# 공공데이터포털(data.go.kr)에서 일반 인증키(Encoding) 발급 필요
def get_VF():
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    serviceKey = '### 일반 인증키 (Encoding) ###'
    time.sleep(0.5)
    params = {'serviceKey': {serviceKey},
              'pageNo': '1',
              'numOfRows': '1000',
              'dataType': 'json',
              'base_date': base_date(),
              'base_time': base_time(),
              'nx': nx,
              'ny': ny}

    response = requests.get(url, params=params)
    return response.content


if __name__ == "__main__":
    # nx, ny의 값을 사용자로부터 받아온다.
    temp = str(input('INSERT YOUR GRID INFO (ex. 96 74) OR ENTER : '))
    if temp != '':
        nx, ny = temp.split()
    del temp

    if ('nx' and 'ny') not in locals():
        # get_nxy 함수를 사용하기 위해서는 city, mdl, leaf 변수가 선언되어야 한다.
        city, mdl, leaf = input('INSERT YOUR ADDRESS (ex. 부산광역시 사하구 하단2동) : ').split()

        # get_nxy 함수를 사용하여 기상청의 격자정보 (nx, ny)를 출력한다.
        nx, ny = get_nxy()
        print(f'YOUR GRID INFO : ({nx}, {ny})\n')

    # 입력된 정보를 통해 기상청에 데이터를 요청하고, 출력한다.
    data = get_VF()
    print(data)
