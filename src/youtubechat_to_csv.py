import pytchat
import datetime
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("video_id", help="Youtube viode ID")
args = parser.parse_args()

# YouTubeのライブ配信またはプレミアム動画のURLまたは動画IDを設定
# video_id = "sp9UV6YSbsI"
video_id = args.video_id

import csv
from os import path

class LocalCsvFile():
    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self.is_exists = path.exists(self.filepath)

    def create(self,headers_list):
        if path.exists(self.filepath):
            raise FileExistsError("もうある")
        try:
            with open(self.filepath, "wt", encoding="utf-8", newline="") as file_object:
                writer = csv.writer(file_object)
                writer.writerow(headers_list)
            return self.filepath
        except Exception as e:
            raise Exception(e)


    def append(self, line):
        # 1行渡すとCSVに1行追記する
        try:
            with open(self.filepath, "a", encoding="utf-8", newline="") as file_object:
                writer = csv.writer(file_object)
                writer.writerow(line)
            return self.filepath
        except Exception as e:
            raise Exception(e)

    def read(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as file_object:
                reader = csv.reader(file_object)
                list_of_rows = list(reader)
                return list_of_rows
        except Exception as e:
            raise Exception(e)

csvfile = LocalCsvFile(f"youtube_{video_id}.csv")

columns = ["datetime","timestamp", "elapsedTime", "type","id","author_name", "isChatSponsor", "message", "amountValue", "amouuntString", "currency"]
try:
    csvfile.create(columns)
except FileExistsError:
    print("作成済み")


chat = pytchat.create(video_id=video_id, topchat_only=False)
tzinfo=datetime.timezone(datetime.timedelta(hours=9))

# 直近n秒間のみのタイムログを保存するリスト
def filter_old_log(loglist, filter_sec):
    nowtime = datetime.datetime.now()

    filtered_logs = []

    for log in loglist:
        # 差がfilter_sec以下の場合、ログを追加する
        if (nowtime - log).total_seconds() <= filter_sec:
            filtered_logs.append(log)
    
    return filtered_logs

btime = datetime.datetime.now()
cnt = 0
chat_per_sec = 0
timelog_list = []

while chat.is_alive():
    before_id = 0

    for c in chat.get().items:
        
        df = pd.DataFrame(csvfile.read(), columns=columns)
        if c.id in df["id"].values:
            break
        timelog_list.append(datetime.datetime.now())
        timelog_list = filter_old_log(timelog_list, 10)
        max_time = max(timelog_list)
        min_time = min(timelog_list)

        if max_time != min_time:
            dif_time = (max(timelog_list) - min(timelog_list)).total_seconds()
        else:
            dif_time = 1
        chat_per_sec = len(timelog_list) / dif_time


        # print("\r"+f"{chat_per_sec}/s\t{c.author.name}:{c.message}",end="")
        print("\r" + f"ChatPerSec : {chat_per_sec:6.2f}/s : count = {len(timelog_list)} : difftime={dif_time}", end="")

        csvfile.append([
            datetime.datetime.fromtimestamp(c.timestamp/1000, tz=tzinfo),
            c.timestamp,
            c.elapsedTime,
            c.type,
            c.id,
            c.author.name,
            c.author.isChatSponsor,
            c.message,
            c.amountValue,
            c.amountString,
            c.currency
        ])