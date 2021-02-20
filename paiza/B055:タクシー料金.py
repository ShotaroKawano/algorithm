#リスト内包表記


# coding: utf-8

# タクシー1: 初乗り: 600m→200円   加算: 200m→400円
# タクシー2: 初乗り: 900m→800円   加算: 400m→500円

# N X
# a_1 b_1 c_1 d_1
# a_2 b_2 c_2 d_2
# ...
# a_N b_N c_N d_N
# ・1 行目にタクシーの種類数 N、目的地までの距離 X がこの順に整数で半角スペース区切りで与えられます。
# ・2 行目から続く N 行には i 番目 (1 ≦ i ≦ N) のタクシーの 初乗り距離 a_i、 初乗り運賃 b_i、 加算距離 c_i、 加算運賃 d_i が整数でこの順にスペース区切りで与えられます。
# ・入力は合計 N + 1 行であり、最終行の末尾に改行が1つ入ります。

# タクシーの料金の最安値と最高値を以下の形式で出力してください。
# P_1 P_2


# 運賃を算出
def cal_fare(X: int, info:list) -> int:
    first_dist = info[0]
    first_fare = info[1]
    add_dist = info[2]
    add_fare = info[3]
    # Xが初乗り距離より小さければ初乗り運賃
    if X < first_dist:
        return first_fare
    # Xが初乗り距離より大きければ初乗り運賃 + (差分と加算距離の商 + 1) × 加算運賃
    # 900 > 500 => 700 + (200 // 400 + 1) * 500
    else:
        return first_fare + ((X - first_dist) // add_dist + 1) * add_fare


# 種類数、距離
N, X = map(int, input().split(" "))
# print(N, X)

# タクシーの運賃情報
info_list = [input() for _ in range(N)]
result = []
for info in info_list:
    info = [int(v) for v in info.split(" ")]
    # info = list(map(int, info.split(" ")))
    result.append(cal_fare(X, info))

# 最大値と最小値を表示
# 事前にソートすればmaxとminしないで済む
print(min(result), end=' ')
print(max(result))
