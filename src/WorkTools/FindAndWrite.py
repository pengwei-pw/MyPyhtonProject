# coding = utf-8
import os
import datetime


def findLongitudeLatitude(log_path:str, start_datetime, end_datetime) -> list:
    start_datetime = datetime.datetime.strptime(start_time, "%m-%d %H:%M:%S.%f")
    end_datetime = datetime.datetime.strptime(end_time, "%m-%d %H:%M:%S.%f")
    print(start_datetime)
    print(end_datetime)
    ll_list = []
    temp_list = []
    for file in os.listdir(log_path):
        if not file.startswith("logcat"):
            continue
        file_path = os.path.join(log_path, file)
        with open(file_path, "r", encoding="MacRoman") as f:
            lines = f.readlines()
            for line in lines:
                try:
                    cur_time = datetime.datetime.strptime(line[:18], "%m-%d %H:%M:%S.%f")
                except ValueError as e:
                    print("当前行非时间戳，跳过")
                    continue

                if cur_time > end_datetime or cur_time < start_datetime:
                    continue
                if line.__contains__("vendor.fnvsoa.gnss: coord_raw_latitude is"):
                    temp_list.append(line.split(" ")[-1])
                elif line.__contains__("vendor.fnvsoa.gnss: coord_raw_longitude is"):
                    temp_list.append(line.split(" ")[-1])
                if len(temp_list) == 2:
                    str_l = f"new BMapGL.Point({temp_list[1].strip()},{temp_list[0].strip()})"
                    ll_list.append(str_l)
                    temp_list.clear()
    return ll_list


def writeTxtByTemplate(info_list, output_template, output_path):
    with open(output_template, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            # print(line)
            start_index = line.find("var points = [];")
            if start_index != -1:
                count_line = i
                # print(i)
    lines[count_line] = "   var points = [" + ",\n".join(f"     {point}" for point in info_list) + "\n  ];\n"
    with open(output_path, "w", encoding="utf=8") as f:
        f.writelines(lines)


if "__main__" == __name__:
    log_path = r"./input"  # 日志路径，日志命名明确logcat.20240515_122111
    output_template = r"./Multi points Baidu coding Template.txt"  # 固定模板信息
    output_path = r"./Multi points Baidu coding.txt"  # 输出文件
    start_time = r"05-15 12:21:17.939"
    end_time = r"05-15 12:22:23.567"
    info_list = findLongitudeLatitude(log_path, start_time, end_time)
    writeTxtByTemplate(info_list, output_template, output_path)


