import csv
import os

def parse_dly_line(line):
    station = line[0:11]
    year = line[11:15]
    month = line[15:17]
    element = line[17:21]

    records = []

    for day in range(31):
        start = 21 + day * 8
        end = start + 8

        if end > len(line):
            break

        raw = line[start:end]
        value = raw[0:5].strip()
        mflag = raw[5]
        qflag = raw[6]
        sflag = raw[7]

        if value == "":
            continue

        day_num = day + 1

        records.append([
            station, year, month, day_num, element, value, mflag, qflag, sflag
        ])

    return records


def dly_to_csv(dly_path, csv_path=None):



    with open(dly_path, "r") as dly_file, open(csv_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["station","year","month","day","element","value","mflag","qflag","sflag"])

        for line in dly_file:
            rows = parse_dly_line(line)
            writer.writerows(rows)

    print(f"Arquivo convertido com sucesso: {csv_path}")


directory = os.fsencode("./data/dly")
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".dly"):

        src = f"./data/dly/{filename}"
        dest = src.replace("dly", "csv")

        dly_to_csv(src, dest)