import csv

char = input("输入汉字：")
if len(char) != 1:
    # if char is not in range(0x4E00, 0x9FA5 + 1):
    #
    char = "我"
temp = ord(char)
# print(char, temp)

csv_path = f"../similiar/{temp}_{char}.csv"
f = open(csv_path, encoding='utf-8')
df = csv.reader(f)
for idx, row in enumerate(df):
    if idx < 2:
        continue
    print(row[1])
