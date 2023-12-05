import ast
import time
from datetime import datetime
import requests
from urllib import parse


# [날짜(YYYYMMDD), 시각(HH00)] 출력 함수
def get_base():
    global base_date, base_time

    base_date = datetime.today().strftime('%Y%m%d')

    # 현재 시각은 정수 형태로, 기상청 단기예보 발표 시각은 리스트 형태로 변수 n, Ann 을 선언한다.
    n = int(str(datetime.now().hour))
    Ann = [2, 5, 8, 11, 14, 17, 20, 23]

    # 기상청 단기예보 발표 시각 중 현재 시각과 가까운 값을 구한다.
    Ann.sort()
    N = min(Ann, key=lambda var: abs(var - n))

    # 값이 현재 시각보다 크면 그 이전의 시각을 구하고, 날짜가 어제가 될 경우 base_date 에 1을 뺀 값을 넣는다.
    if N < n or (N == n and datetime.now().minute > 10):
        x = N
    else:
        if N - 3 < 0:
            x = Ann[-1]
            base_date = str(ast.literal_eval(base_date)-1)
        else:
            x = N-3

    if x >= 10:
        base_time = f'{x}00'
    else:
        base_time = f'0{x}00'

    return base_date, base_time


# [A시 B구 C동] -> [기상청 격자정보 (nx, ny)] 치환 함수
# 다음의 변수 선언이 선행되어야 한다. [city, mdl, leaf]
def get_nxy():
    global nx, ny

    # 변수 city, mdl, leaf 값을 value 값으로 가지는 딕셔너리를 찾고, key 값이 "code"인 value 값을 가져온다.
    response1 = ast.literal_eval(
        requests.get(f'https://www.kma.go.kr/DFSROOT/POINT/DATA/top.json.txt').content.decode('utf-8'))
    city_code = [str(response1[i].get('code')) for i in range(len(response1)) if city in response1[i].values()][0]

    response2 = ast.literal_eval(
        requests.get(f'https://www.kma.go.kr/DFSROOT/POINT/DATA/mdl.{city_code}.json.txt').content.decode('utf-8'))
    mdl_code = [str(response2[j].get('code')) for j in range(len(response2)) if mdl in response2[j].values()][0]

    response3 = ast.literal_eval(
        requests.get(f'https://www.kma.go.kr/DFSROOT/POINT/DATA/leaf.{mdl_code}.json.txt').content.decode('utf-8'))

    for k in range(len(response3)):
        if leaf in response3[k].values():
            nx = str(response3[k].get('x'))
            ny = str(response3[k].get('y'))
            break

    return nx, ny


# 기상청 단기예보(dataType==json, type==dict) 출력 함수
# 다음의 변수 선언이 선행되어야 한다. [base_date, base_time, nx, ny]
def get_VF():
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    ServiceKey = '### 일반 인증키 (Encoding) ###'

    params = (f'?{parse.quote_plus("ServiceKey")}={ServiceKey}&' +
              parse.urlencode({
                  parse.quote_plus('pageNo'): '1',
                  parse.quote_plus('numOfRows'): '1000',
                  parse.quote_plus('dataType'): 'json',
                  parse.quote_plus('base_date'): base_date,
                  parse.quote_plus('base_time'): base_time,
                  parse.quote_plus('nx'): nx,
                  parse.quote_plus('ny'): ny
              }))

    response = requests.get(url + params, verify=False).json().get('response').get('body').get('items').get('item')

    return response


# 강수가 일어날 시간대와 강수확률을 출력한다.
# val 값이 0이면 오늘, 1이면 내일, 2이면 모레의 값을 나타낸다.
def rainfall(response, val):
    POP = []

    if val == 0:
        for i in response:
            if i['category'] == 'POP' and i['fcstDate'] == base_date:
                if i['fcstValue'] != '0':
                    POP.append(i)
        if POP == []:
            print('오늘은 우산이 필요없는 날입니다.')
        else:
            print('오늘 강수가 일어날 시간대는 아래와 같습니다.')
        for j in POP:
            print(f"{j['fcstTime']} : 강수확률은 {j['fcstValue']}%")

    elif val == 1:
        for i in response:
            if i['category'] == 'POP' and i['fcstDate'] == str(ast.literal_eval(base_date)+1):
                if i['fcstValue'] != '0':
                    POP.append(i)
        if POP == []:
            print('내일은 우산이 필요없는 날입니다.')
        else:
            print('내일 강수가 일어날 시간대는 아래와 같습니다.')
        for j in POP:
            print(f"{j['fcstTime']} : 강수확률은 {j['fcstValue']}%")

    elif val == 2:
        for i in response:
            if i['category'] == 'POP' and i['fcstDate'] == str(ast.literal_eval(base_date)+2):
                if i['fcstValue'] != '0':
                    POP.append(i)
        if POP == []:
            print('모레는 우산이 필요없는 날입니다.')
        else:
            print('모레 강수가 일어날 시간대는 아래와 같습니다.')
        for j in POP:
            print(f"{j['fcstTime']} : 강수확률은 {j['fcstValue']}%")

    print()


if __name__ == "__main__":
    base_date, base_time = get_base()

    temp = str(input('INSERT YOUR GRID INFO (ex. 96 74) OR ENTER : '))
    if temp != '':
        nx, ny = temp.split()
        print(f'YOUR GRID INFO : ({nx}, {ny})\n')
    del temp

    if ('nx' and 'ny') not in locals():
        city, mdl, leaf = input('INSERT YOUR ADDRESS (ex. 부산광역시 사하구 하단2동) : ').split()
        nx, ny = get_nxy()
        print(f'YOUR GRID INFO : ({nx}, {ny})\n')

    try:
        res = get_VF()
    except Exception as e:
        print('SOMETHING WENT WRONG...')

        res = get_VF()
        while 'errMsg' in res:
            res = get_VF()
            time.sleep(5)

        if 'errMsg' not in res:
            print('SUCCEED!')

    refine_res = input('오늘, 내일, 모레 중 강수가 일어날 시간대를 알고 싶은 날을 모두 입력하세요 : ')
    if '오늘' in refine_res:
        rainfall(res, 0)
    if '내일' in refine_res:
        rainfall(res, 1)
    if '모레' in refine_res:
        rainfall(res, 2)
