from datetime import datetime


# 입력값을 {날짜 시간, 메모} 딕셔너리로 calist 리스트에 추가한다.
# 만약 날짜가 동일한 딕셔너리가 있으면, 기존 메모 바로 뒤에 새로운 메모를 더한다.
# cal_list = [] 가 이전에 명령되어야 한다.
def memo(some):
    ymd, hm, memo_some = some.split(' ', maxsplit=2)
    ymd_hm = ymd + ' ' + hm

    legacy_memo = 'temp'
    for i in cal_list:
        if i.get(ymd_hm) is not None:
            legacy_memo = i.get(ymd_hm)

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

    today_list = []
    for i in some_list:
        if ymd in str(i.keys()):
            today_list.append(list(i.values())[0])

    now_list = []
    for j in some_list:
        if ymd_hm in str(j.keys()):
            now_list.append(list(j.values())[0])

    return today_list, now_list


if __name__ == "__main__":
    cal_list = []

    while True:
        while True:
            what2do = input('1. MEMO / 2. DEL / 3. CHECK (TAP NUM) : ')

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
            elif what2do == '4':
                break

        print(cal_list)
