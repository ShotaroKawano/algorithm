#回数入力 #複数行入力 #数値入力

# ================================================================================
# 最初にチャージする現金と、バスを利用した時にかかった料金のリストが与えられるので、毎回の降車時に残っているお金とポイントを出力してください。
# バスの運賃支払に paica のカード残額を使うと、運賃の 10 % が paica ポイントとしてたまります。

# 入力例
# (初回チャージ金額) (乗車回数)
# 2000 5
# (運賃)
# 300
# 500
# 300
# 100
# 100

# 出力例
# (残高) (ポイント)
# 1700 30
# 1200 80
# 900 110
# 900 10
# 800 20



# ================================================================================
# coding: utf-8

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
