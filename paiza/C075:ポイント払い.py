# coding: utf-8
# 自分の得意な言語で
# Let's チャレンジ！！

balance, count = map(int, input().split())
point = 0
# print(balance)
# print(count)
# print(point)

# fare_list = []
for i in range(0, count):
    fare = int(input())
#   if fare:
#     fare_list.append(int(fare))

    if point < fare:
        balance = balance - fare
        point = point + int(fare * 0.1)
    else:
        point = point - fare

    print(balance, point)
