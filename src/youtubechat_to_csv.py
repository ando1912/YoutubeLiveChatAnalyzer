import sys
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

while chat.is_alive():
    before_id = 0
    for c in chat.get().items:
        
        df = pd.DataFrame(csvfile.read(), columns=columns)
        if c.id in df["id"].values:
            break

        print(f"{c.author.name}:{c.message}")

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