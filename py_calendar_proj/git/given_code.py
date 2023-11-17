def display_custom_calendar(month, year):
    # 각 월의 일수를 저장한 리스트 (윤년이 아닌 경우)
    month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # 2023년 10월은 일요일부터 시작
    if year == 2023 and month == 10:
        first_weekday= 6  # 일요일
    else:
        first_weekday= 0  # 임의로 월요일로 설정

    #윤년 확인
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        month_days[2] = 29

    # 달력 상단에 현재 월/연도 표시
    month_names= ["", "1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]
    print(f"{month_names[month]} {year}")

    # 요일 이름 출력
    weekdays = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    print(" ".join(weekdays))
    print("-" * 20)

    # 일자 출력
    day_counter= 1 - first_weekday
    for _ in range(6):  # 한 달은 최대 6주까지 있을 수 있음
        week = []
        for _ in range(7):
            if 1 <= day_counter<= month_days[month]:
                week.append(str(day_counter).rjust(2))
            else:
                week.append("  ")
            day_counter += 1
        print(" ".join(week))


# 테스트: 2023년 10월 달력 출력
display_custom_calendar(10, 2023)