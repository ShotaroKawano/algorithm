# 単体テスト #実験 #unittest.TestCase

# ================================================================================
# 日付が入力されるのでその日付の 1 日前を出力してください。
# 入力例1
# 25
# 出力例1
# 24



# ================================================================================
# coding: utf-8

# 回答
def calcEve(day:int) -> int:
    return day - 1

day = int(input())
print(calcEve(day))


# 単体テストの実験
import unittest

class EveTest(unittest.TestCase):

    def test_calc_eve(self):
        # 繰り返す場合
        for (expected, actual) in [(1, 2), (24, 25)]:
            self.assertEqual(expected, calcEve(actual))

        # 一行ずつ書く方がコメントアウトしやすい
        self.assertEqual(1, calcEve(2))
        # self.assertEqual(23, calcEve(25))
        self.assertEqual(24, calcEve(25))
        # わざと AssertionError を起こさないとテストのログが見れない
        self.assertEqual(1, 2)

unittest.main()
