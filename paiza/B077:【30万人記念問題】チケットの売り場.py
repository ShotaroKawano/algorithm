#filter #All(python)==every(js) #sort #オブジェクトのリスト内包表記 #オブジェクト指向 #自然言語 #状態 #再帰的

# ================================================================================
# 問題
# ここのチケット売り場には N 個のカウンターがあります。
# i 番目のカウンターは処理に t_i の時間がかかります。
# ここでは複数のカウンターに対してひとつの列で並び、空いたカウンターに先頭の人が行きます。ただし、空いたカウンターに移動する時間は考慮しないものとします。
# また、複数のカウンターが空いている場合はより処理時間の短いカウンターに行くものとします。
# M 人並んでいるとき、全員がチケットを買い終わるまでかかる時間を答えてください。ただし、総客数はカウンター数以上であるものとします。

# 入力例 1 では、時刻 0 に最初の 3 人が 1, 2, 3 番目のカウンターに行きます。
# 次に時刻 2 に 1 番目のカウンターが空くので、 4 人目が同時刻に 1 番目のカウンターで処理を開始します。
# 次に時刻 4 に 5, 6 人目が 1, 2 番目のカウンターに行きます。
# このようにして時刻 8 に全員がチケットを買い終わります。

# ・1 行目にチケット売りのカウンターの数を表す整数 N と並んでいる人数を表す整数 M が半角スペース区切りで与えられます。
# ・i 行目 (1 ≦ i ≦ N) に i 番目のカウンターでチケットを買うのにかかる時間 t_i を表す整数が与えられます。

# 入力例1
# 3 6
# 2
# 4
# 5

# 出力例1
# 8


# 方針
# - 処理時間を累積してもっとも大きい累積処理時間を計算する

# 1.処理情報を辞書の配列で管理
# 2.並んでいる人がいなくなるまでループ
#   2-1.累積処理時間が最小のカウンターに処理時間を加算
# 3.もっとも大きい累積処理時間を返す

# メモ
# - 人数か時間でループするか迷うところだが、処理時間を累積するやり方だと
# - 時間をループする必要がないのがすごい



# ================================================================================
# 吉島さんのやり方
# coding: utf-8

num_counter, num_people = map(int, input().split())
processing_time_list = [int(input()) for _ in range(num_counter)]

# 処理時間が短い順にソート
processing_time_list.sort()
# カウンターの処理情報辞書を格納する配列
counters = []

# [方法1]処理情報辞書を格納
for i in range(num_counter):
    counter = {
        'id': i,
        'processing_time': processing_time_list[i],
        'accumulated_time': processing_time_list[i]
    }
    counters.append(counter)

# [方法2]処理情報辞書を格納
# counters = \
#     [
#         {
#             'id': i,
#             'processing_time': processing_time_list[i],
#             'accumulated_time': processing_time_list[i]
#         } for i in range(num_counter)
#     ]


def calc_comp_time(num_counter, num_people, counters):
    # 並んでいる人の数
    num_waitings = num_people - num_counter
    # 並んでいる人がいなくなるまでループ
    while(num_waitings > 0):
        # 累積処理時間のリストを作成し、最小値を取得
        accumulated_time_list = [ counter['accumulated_time'] for counter in counters ]
        min_accumulated_time = min(accumulated_time_list)
        # 最長値のインデックスを取得
        vacant_index = accumulated_time_list.index(min_accumulated_time)

        # 上記のインデックスを用いて、累積処理時間がもっとも小さいカウンターに処理時間を加算
        counters[vacant_index]['accumulated_time'] += counters[vacant_index]['processing_time']
        # 並んでいる人を一人減らす
        num_waitings -= 1

    # 累積処理時間がもっとも大きい数値が全員がチケットを買い終わるまでにかかる時間
    return max([ counter['accumulated_time'] for counter in counters ])


complete_time = calc_comp_time(num_counter, num_people, counters)
print(complete_time)



# ================================================================================
# TDさんのやり方
# 注意！：入力例はすべて成功するが、テストケースはすべて失敗する

# // 方針
# // chaserクラスを作ってそれらをcasherControllerクラスで操作する
# // タスクがあるかないか確認する
# // すべてのキャッシャーが作業中かどうか判断する
# // タスクがあるなら作業中でないキャッシャーにタスクを割り振る
# // すべてのキャッシャーのプロセス時間を更新する
# // タスクがすべて終わっている && キャッシャーがすべて停止している状態なら時間を出力する
# // そうでなければ以上をくり返す

# coding: utf-8

import sys

# // casherクラス
# // 作業にかかる時間・現在のタスクにかかっている時間・作業中かどうかの状態を持つ
# // 現在のタスクにかかっている時間を更新する処理
class Counter:

    def __init__(self, processing_time):
        self.processing_time = processing_time
        self.accumulated_time = 0
        self.is_processing = False


    def start_process(self):
        self.is_processing = True


    def finish_process(self):
        self.is_processing = False


    def get_is_processing(self):
        return self.is_processing == True


    # 冗長な関数定義だが、後のロジックで自然言語的に読めるコードが書ける
    def get_is_sleeping(self):
        return self.is_processing == False


    def update(self):
        # 累積処理時間が1ずつ増やす 割り切れたら0に戻る
        # processing_time = 5 のとき accumulated_time の変化は 1→2 / 4→0
        self.accumulated_time = (self.accumulated_time + 1) % self.processing_time
        if self.accumulated_time == 0:
            self.finish_process()


    def __str__(self):
        return str([self.processing_time, self.accumulated_time, self.is_processing])


# // CasherController クラス
# // キャッシャーのインスタンス・タスク・現在の時間の状態を持つ
# // 時間を更新するメソッド キャッシャーを更新するメソッドを持つ
class CounterController:

    def __init__(self, num_people, counters):
        self.num_people = num_people
        self.counters = counters
        self.time = 0


    def get_has_task(self):
        return self.num_people > 0


    def get_has_not_task(self):
        return self.num_people == 0


    def get_is_every_counter_sleeping(self):
        is_processing_list = [ counter.get_is_sleeping() for counter in self.counters ]
        # ()内の真偽値がすべてTrueのときTrueになる jsのeveryと同じ
        return all(is_processing_list)


    def get_is_all_complete(self):
        return self.get_has_not_task() and self.get_is_every_counter_sleeping()


    def set_task(self):
        if self.get_has_not_task():
            return
        # filter(関数, リスト)
        filtered_counters = filter(lambda x:x.get_is_sleeping(), self.counters)
        for counter in filtered_counters:
            if self.get_has_task():
                counter.start_process()
                self.num_people -= 1


    def update_cashers(self):
        # filter(関数, リスト)
        filtered_counters = filter(lambda x:x.get_is_processing(), self.counters)
        for counter in filtered_counters:
            counter.update()


    def invoke(self):
        self.set_task()
        # print(str(counter_controller))
        self.update_cashers()
        self.time += 1
        if self.get_is_all_complete():
            self.print_result()
        else:
            self.invoke()
    # # ループに書き直したバージョン
    # def invoke(self):
    #     while(not self.get_is_all_complete()):
    #         self.set_task()
    #         self.update_cashers()
    #         self.time += 1
    #     self.print_result()


    def print_result(self):
        print(self.time)


    def __str__(self):
        return str([ str(counter) for counter in self.counters ])



num_counter, num_people = map(int, input().split())
processing_time_list = [int(input()) for _ in range(num_counter)]
counters = []

# 再帰回数制限対策（# RecursionError: maximum recursion depth exceeded in comparison）
# print(sys.getrecursionlimit())
# depthのため保険の+1 これがないと入力例3でエラーになる
sys.setrecursionlimit(num_people * max(processing_time_list) + 1)
# print(sys.getrecursionlimit())

for processing_time in processing_time_list:
    counters.append(Counter(processing_time))

sorted_counters = sorted(counters, key=lambda x:x.processing_time)

counter_controller = CounterController(
    num_people,
    sorted_counters
)

counter_controller.invoke()




# ================================================================================
# 学んだこと
# is_processingとis_sleepingのように冗長だがtrueを返すように関数を定義すると自然言語的に読めるコードになる
# 無間ループの原因になるのでなるべくwhileは使わない
# 複雑性をオブジェクト指向で解決できる まさにオブジェクト至高
# クラスで書けば単体テストできるのでメンテナンス性が高い
# jsからpythonに書き換えたので関数の()忘れでバグを生みまくった jsのcallbackで()なしで渡している部分につられた
# 無制限に再帰処理をしてスタックオーバーフローを起こさないようにpythonでは再帰処理の階層がデフォルトで1000までに制限されている
# - https://stackoverflow.com/questions/3323001/what-is-the-maximum-recursion-depth-in-python-and-how-to-increase-it
# 各言語で再帰処理の制限値が設けられているので、これまで動いていたものが唐突に動かなくなる可能性がある
# 入力例で成功してテストケースすべてで失敗する場合は再帰回数エラーのようにテストケースでの試行回数やデータ量に対応できていない可能性がある
# 再帰回数エラーの正しい対処法はループに書き直す