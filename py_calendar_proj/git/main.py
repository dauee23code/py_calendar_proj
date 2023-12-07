import ast
import random
import time
from datetime import datetime
import requests
from urllib import parse


def display_custom_calendar(month, year):
    # 각 월의 일수를 저장한 리스트 (윤년이 아닌 경우)
    month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # 2023년 10월은 일요일부터 시작
    if year == 2023 and month == 10:
        first_weekday = 6  # 일요일
    else:
        first_weekday = 0  # 임의로 월요일로 설정

    # 윤년 확인
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        month_days[2] = 29

    # 달력 상단에 현재 월/연도 표시
    month_names = ["", "1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]
    print(f"{month_names[month]} {year}")

    # 요일 이름 출력
    weekdays = ["\033[92mMo\033[0m", "\033[92mTu\033[0m", "\033[92mWe\033[0m", "\033[92mTh\033[0m", "\033[92mFr\033[0m",
                "\033[94mSa\033[0m", "\033[91mSu\033[0m"]
    print(" ".join(weekdays))
    print("-" * 20)

    # 일자 출력 # ANSI Escape Code
    day_counter = 1 - first_weekday
    for _ in range(6):  # 한 달은 최대 6주까지 있을 수 있음
        week = []
        for _ in range(7):
            if 1 <= day_counter <= month_days[month]:
                # 예를 들어, day_counter가 1이고 first_weekday가 2라면, 실제 출력되어야 하는 날짜는 월요일이 됩니다.
                # 따라서 day_counter + first_weekday는 3이 되어 월요일을 나타내게 됩니다.
                if (first_weekday + day_counter) % 7 == 6:
                    day_str = "\033[94m" + str(day_counter).rjust(2) + "\033[0m"
                elif (first_weekday + day_counter) % 7 == 0:
                    day_str = "\033[91m" + str(day_counter).rjust(2) + "\033[0m"
                else:
                    day_str = "\033[92m" + str(day_counter).rjust(2) + "\033[0m"
                week.append(day_str)
            else:
                week.append("  ")
            day_counter += 1
        print(" ".join(week))


def option_1():
    def get_special_fortune(year, month, day):
        # 특별한 날짜에 대한 운세를 반환하는 함수
        if month == 10 and day == 31:
            return "할로윈!"
        return None

    def get_daily_fortune(date):
        fortunes = [
            "오늘은 행복한 날이 될 것 같음.",
            "긍정적인 에너지가 가득한 하루가 될 거임.",
            "어제보다 더 나은 일이 기다리고 있음.",
            "좋은 소식이 당신을 기다리고 있음.",
            "뜻하지 않은 기회가 찾아올 것 같음.",
            "스트레스를 떨쳐내고 즐거운 순간을 즐겨보셈.",
            "주변 사람들과의 소통이 풍부한 하루가 될 거임."
        ]
        if 1 <= date <= 31:
            selected_fortune = random.choice(fortunes)
            special_fortune = get_special_fortune(2023, 10, date)
            if special_fortune:
                print(f"{date}일의 특별한 운세: {special_fortune}")
            else:
                print(f"{date}일의 운세: {selected_fortune}")
        else:
            print("올바른 날짜 범위(1 ~ 31)의 값을 입력하세요.")

    n = input('오늘의 운세를 알고 싶어요? (Y/N): ')
    if n == "Y":
        # 사용자로부터 날짜 입력 받기
        date = int(input("오늘은 몇 일인가요? (1 ~ 31): "))
        # 운세 가져오기 및 출력
        get_daily_fortune(date)
    if n == "N":
        print('다음에 하세요!')


def option_2():
    # 입력값을 {날짜 시간, 메모} 딕셔너리로 calist 리스트에 추가한다.
    # 만약 날짜가 동일한 딕셔너리가 있으면, 기존 메모 바로 뒤에 새로운 메모를 더한다.
    # cal_list = [] 가 이전에 명령되어야 한다.
    def memo(some):
        ymd, hm, memo_some = some.split(' ', maxsplit=2)
        ymd_hm = ymd + ' ' + hm

        legacy_memo = 'temp'
        for i in cal_list:
            # 동일한 날짜 시간의 메모가 있으면 그 값(메모)를 다른 변수에 저장한다.
            if i.get(ymd_hm) is not None:
                legacy_memo = i.get(ymd_hm)

        # 동일한 날짜 시간의 메모가 있으면 그 값을 지우고, 기존 메모와 새로운 메모를 합친 딕셔너리를 리스트에 저장한다.
        if legacy_memo != 'temp':
            cal_list.remove({ymd_hm: legacy_memo})
            cal_list.append({ymd_hm: legacy_memo + memo_some})
        else:
            cal_list.append({ymd_hm: memo_some})

        del ymd_hm, memo_some, legacy_memo

    # 입력된 날짜 시간이 key 값인 딕셔너리를 삭제한다.
    def del_memo(some):
        ymd, hm = some.split(' ', maxsplit=1)
        ymd_hm = ymd + ' ' + hm

        j = -1
        for i in cal_list:
            j += 1
            if ymd_hm in i:
                del cal_list[j]

        del ymd_hm

    # 리스트에 있는 키 값(날짜)을 참조하여 오늘 해야할 일과 지금 해야할 일을 반환한다.
    def checker(some_list):
        ymd, hm = datetime.now().strftime('%Y.%m.%d %H:%M:%S').split()
        ymd_hm = ymd + ' ' + hm

        # 날짜가 같은 메모들을 모두 불러와서 today_list에 저장한다.
        today_list = []
        for i in some_list:
            if ymd in str(i.keys()):
                today_list.append(list(i.values())[0])

        # 날짜와 시간이 모두 같은 메모들을 모두 불러와서 now_list에 저장한다.
        now_list = []
        for j in some_list:
            if ymd_hm in str(j.keys()):
                now_list.append(list(j.values())[0])

        return today_list, now_list

    cal_list = []

    while True:
        what2do = input('1. MEMO / 2. DEL / 3. CHECK / 4. Exit (TAP NUM) : ')

        if (what2do == '1') or (what2do == 'MEMO'):
            memo(input('MEMO (ex. 1999.12.31 12:00 세기말) : '))
            continue
        elif (what2do == '2') or (what2do == 'DEL'):
            del_memo(input('YYYY.MM.DD HH:mm (ex. 1999.12.31 12:00) : '))
            continue
        elif (what2do == '3') or (what2do == 'CHECK'):
            tod_do, now_do = checker(cal_list)
            print(f'오늘 해야할 일 : {tod_do}')
            print(f'지금 해야할 일 : {now_do}')
            continue
        elif (what2do == '4') or (what2do == 'Exit'):
            break

    print(cal_list)


def option_3():
    # [날짜(YYYYMMDD), 시각(HH00)] 출력 함수
    def get_base():
        fcst_base_date = datetime.today().strftime('%Y%m%d')

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
                fcst_base_date = str(ast.literal_eval(fcst_base_date) - 1)
            else:
                x = N - 3

        if x >= 10:
            fcst_base_time = f'{x}00'
        else:
            fcst_base_time = f'0{x}00'

        return fcst_base_date, fcst_base_time

    # [A시 B구 C동] -> [기상청 격자정보 (nx, ny)] 치환 함수
    # 다음의 변수 선언이 선행되어야 한다. [city, mdl, leaf]
    def get_nxy():
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
                fcst_nx = str(response3[k].get('x'))
                fcst_ny = str(response3[k].get('y'))
                break

        return fcst_nx, fcst_ny

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
            if not POP:
                print('오늘은 우산이 필요없는 날입니다.')
            else:
                print('오늘 강수가 일어날 시간대는 아래와 같습니다.')
            for j in POP:
                print(f"{j['fcstTime']} : 강수확률은 {j['fcstValue']}%")

        elif val == 1:
            for i in response:
                if i['category'] == 'POP' and i['fcstDate'] == str(ast.literal_eval(base_date) + 1):
                    if i['fcstValue'] != '0':
                        POP.append(i)
            if not POP:
                print('내일은 우산이 필요없는 날입니다.')
            else:
                print('내일 강수가 일어날 시간대는 아래와 같습니다.')
            for j in POP:
                print(f"{j['fcstTime']} : 강수확률은 {j['fcstValue']}%")

        elif val == 2:
            for i in response:
                if i['category'] == 'POP' and i['fcstDate'] == str(ast.literal_eval(base_date) + 2):
                    if i['fcstValue'] != '0':
                        POP.append(i)
            if not POP:
                print('모레는 우산이 필요없는 날입니다.')
            else:
                print('모레 강수가 일어날 시간대는 아래와 같습니다.')
            for j in POP:
                print(f"{j['fcstTime']} : 강수확률은 {j['fcstValue']}%")

        print()

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


def input_option():
    print("1. 오늘의 운세 확인하기!")
    print("2. 두 번째 옵션")
    print("3. 세 번째 옵션")

    while True:
        choice = input("실행할 옵션의 번호를 입력하세요: ")

        if choice == '1':
            option_1()
        elif choice == '2':
            option_2()
        elif choice == '3':
            option_3()
        else:
            print("올바른 옵션 번호를 입력하세요.")


if __name__ == "__main__":
    # 테스트: 2023년 10월 달력 출력, 생일 정보와 메모 포함
    display_custom_calendar(10, 2023)
    input_option()
