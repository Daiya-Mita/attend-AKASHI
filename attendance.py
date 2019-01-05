import argparse
import requests
import datetime as dt
import jpholiday


# config
token = ""


def parser():
    parser = argparse.ArgumentParser(description="これは出勤,退勤用のscriptとなります.")
    parser.add_argument("punch_type", type=int, help=":11なら出勤、12なら退勤")
    args = parser.parse_args()
    return args.punch_type


def punch(punch_type: int):
    endpoint = "https://atnd.ak4.jp/api/cooperation"
    compid = ""
    r = requests.post("{}/{}/stamps?token={}&type={}".format(endpoint, compid, token, str(punch_type)))
    for k, v in r.json().items():
        print(k, ":", v)


if __name__ == "__main__":
    punch_type = parser()

    now = dt.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    today = dt.date(year, month, day)

    is_holiday = jpholiday.is_holiday(today)
    is_weekend = True if today.weekday() >= 5 else False
    custom_holiday_list = [(12, 31), (1, 1), (1, 2), (1, 3)]
    is_custom_holiday = True if (month, day) in custom_holiday_list else False

    # とりあえず休日出勤しない仕様に
    if is_holiday is False and is_weekend is False and is_custom_holiday is False:
        punch(punch_type)
