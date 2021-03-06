#set #集合 #検証 #単体テスト


# coding: utf-8

# ポーカーの手役を判定するプログラム
# ルールは以下+ジョーカー1枚
# https://www.nintendo.co.jp/others/playing_cards/howtoplay/poker/index.html

from enum import Enum, IntEnum
import datetime


class Suit(Enum):
    # マークはunicodeで扱った方がどの環境でも文字化けしなそう
    # Rankや手役もenumの方が安全
    SPADE = 1
    HEART = 2
    DIAMOND = 3
    CLUB = 4
    JOKER = 0

    def __str__(self):
        suits = ['🃏', '♠', '♥', '♦', '♣']
        return suits[self.value]

# IntEnumで整数として扱うのもあり、ただし文字列で値を保持できない
# 数値同士の大小関係をメソッドとして定義したりもできる
# ACEを14として扱うべきか？
class Rank(IntEnum):
    ACE = 1
    R2 = 2
    R3 = 3
    R4 = 4
    R5 = 5
    R6 = 6
    R7 = 7
    R8 = 8
    R9 = 9
    R10 = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    JOKER = 0

    # ACE = 1
    # TWO = 2
    # THREE = 3
    # FOUR = 4
    # ...
    # JACK = 11
    # QUEEN = 12
    # KING = 13
    # JOKER = 0

    # Enumの場合
    # KING = 'J'
    # JOKER = '0'
    # _2 = '2'
    # N2 = '2'

    def __str__(self):
        if self.value == 1:
            return 'A'
        elif self.value == 11:
            return 'J'
        elif self.value == 12:
            return 'Q'
        elif self.value == 13:
            return 'K'
        elif self.value == 0:
            return '*'
        else:
            return str(self.value)


class Card(object):
    def __init__(self, suit, rank):
    # def __init__(self, suit: Suit, rank: Rank):
        # マーク
        self.suit = suit
        # 数字(ジョーカーは0 数字で扱うとソートが使える)
        self.rank = rank
        # rankでenumを使用しない場合はここで入力検証
        # if rank >= 0 and rank < 14:
        #     self.rank = rank
        # else:
        #     raise ValueError

    # __str__は、人間にとってわかりやすい文字列を返す
    def __str__(self):
        return f'{str(self.suit)} {str(self.rank):2s}'
        # return str(self.suit) + ' ' + str(self.rank)
        # return self.suit.value + ' ' + str(self.rank)

    # __repr__は、Pythonが復元できる(evalで評価すると元のオブジェクトに戻る)文字列を返す
    def __repr__(self):
        return f'Card({self.suit.value}, {str(self.rank)})'


# まずジョーカーなしの手役判定メソッド
def determine_hand1(hand):
    # 手札のrankリスト
    rank_list = sorted([ card.rank for card in hand ])
    # print(rank_list)

    # カードの種類数(setは重複を取り除く)
    rank_set_size = len(set(rank_list))
    # print(rank_set_size)

    # 確率が高いペア系かどうかの判定を先にする
    # ペア系: FourCard, FullHouse, ThreeCard, TwoPair, OnePair
    # ペア系の中では確率の高いOnePairの方から判定した方が高速
    # 3階層で分岐が多いので2階層に収めたい

    # カードにダブりがあるとrank_set_sizeは5未満になる ['♥ 12', '♣ 12', '♥ 2', '♦ 2', '♣ 7']
    if rank_set_size < 5:
        if rank_set_size == 2:
            # 個数が1のカードが存在する場合 ['♠ 8', '♥ 8', '♦ 8', '♣ 8', '♦ 2']
            if 1 in [ rank_list.count(rank) for rank in rank_list ]:
                return 'FourCard'
            # すべての個数が2以上の場合 ['♠ 6', '♥ 6', '♣ 6', '♦ 3', '♣ 3']
            else:
                return 'FullHouse'
        elif rank_set_size == 3:
            # 個数が1のカードが2枚存在する場合 ['♠ 9', '♥ 9', '♦ 9', '♠ 12', '♣ 7']
            if [ rank_list.count(rank) for rank in rank_list ].count(1) == 2:
                return 'ThreeCard'
            # 上記以外
            else:
                return 'TwoPair'
        elif rank_set_size == 4:
            return 'OnePair'

    # rank_set_size = 5 のとき
    else:
        isFlush = False
        # 手札のsuitリスト
        suit_list = [ card.suit.name for card in hand ]
        # print(suit_list)

        # フラッシュ(手札がすべて1番目のsuitと同じ)か？
        if suit_list.count(suit_list[0]) == 5:
            isFlush = True

        # フラッシュ かつ [10, J, Q, K, A]の組み合わせ
        if isFlush and rank_list == [1, 10, 11, 12, 13]:
            return 'RoyalFlush'

        # 注意：フラッシュでない[1, 10, 11, 12, 13]の組み合わせが抜け落ちがち(↓に実装は抜け落ちている)
        # Aと2がつながらない前提で、Aを14として扱えば良い
        isStraght = rank_list[0] + 1 == rank_list[1] and rank_list[1] + 1 == rank_list[2] and rank_list[2] + 1 == rank_list[3] and rank_list[3] + 1 == rank_list[4]

        if isStraght and isFlush:
            return 'StraightFlush'
        elif isFlush:
            return 'Flush'
        elif isStraght:
            return 'Straight'
        else:
            return 'NoPair'


# ================================================================================


# 全体的にリーダブルだけどMECEかすぐにわからない
def determine_hand2(hand):
    # 手札のrankリスト
    rank_list = sorted([ card.rank for card in hand ])
    # 手札のsuitリスト
    suit_list = [ card.suit.name for card in hand ]
    # 手札の数字の個数リスト [1, 4, 4, 4, 4] ← ['♠ 8', '♥ 8', '♦ 8', '♣ 8', '♦ 2']
    rank_count_list = [ rank_list.count(rank) for rank in rank_list ]
    # print(rank_count_list)
    # 手札の数字集合
    rank_set = set(rank_list)
    # print(rank_set)
    # 手札の数字の種類数(setは重複を取り除く、ジョーカーを1としてカウント)
    rank_set_size = len(rank_set)
    # ジョーカーありなしのフラグ
    isJokerExists = Suit.JOKER.name in suit_list

    # ペアが存在する場合
    # FourCard, FullHouse, ThreeCard, TwoPair, OnePair
    if rank_set_size < 5:

        # ジョーカーあり かつ 個数3か4のカードが存在 ['♠ 8', '🃏 0', '♦ 8', '♣ 8', '♦ 2']
        # or ジョーカーなし かつ 個数4のカードが存在 ['♠ 8', '♥ 8', '♦ 8', '♣ 8', '♦ 2']
        # FiveCard はなしのルール
        if (isJokerExists and (rank_count_list.count(4) == 4 or rank_count_list.count(3) == 3)) \
            or (not isJokerExists and rank_count_list.count(4) == 4):
            return 'FourCard'
        # if (isJokerExists and (rank_count_list.count(4) > 1 or rank_count_list.count(3) > 1)) \
        #     or (not isJokerExists and rank_count_list.count(4) > 1):
        #     return 'FourCard'

        # ジョーカーあり かつ 個数2のカード2種類(2枚ずつ4枚)存在 ['🃏 0', '♥ 6', '♣ 6', '♦ 3', '♣ 3']
        # or ジョーカーなし かつ 個数2と3のカードが存在 ['♠ 6', '♥ 6', '♣ 6', '♦ 3', '♣ 3']
        if (isJokerExists and rank_count_list.count(2) == 4) \
            or (not isJokerExists and rank_count_list.count(3) == 3 and rank_count_list.count(2) == 2):
            return 'FullHouse'

        # ジョーカーあり かつ カードの種類が4(ペアが1つ) ['♠ 9', '🃏 0', '♦ 9', '♠ 12', '♣ 7']
        # or ジョーカーなし かつ カードの種類が3 かつ 個数1のカードが2枚 ['♠ 9', '♥ 9', '♦ 9', '♠ 12', '♣ 7']
        if (isJokerExists and rank_set_size == 4) \
            or not isJokerExists and rank_set_size == 3 and rank_count_list.count(1) == 2:
            return 'ThreeCard'

        # ジョーカーありのときはTwoPairはない ThreeCardになる
        # ジョーカーなし かつ カードの種類が3 ['♥ 12', '♣ 12', '♥ 2', '♦ 2', '♣ 7']
        if not isJokerExists and rank_set_size == 3:
            return 'TwoPair'

        # ジョーカーありのときはOnePairは rank_set_size = 5 になるためelse文の★で処理
        # ★ ジョーカーなし かつ カードの種類が4 ['♦ 3', '♣ 3', '♠ 11', '♥ 4', '♦ 1']
        if not isJokerExists and rank_set_size == 4:
            return 'OnePair'

    # すべてのカードが異なる場合(rank_set_size = 5)
    # RoyalFlush, StraightFlush, Flush, Straight, NoPair
    else:
        # フラッシュフラグ
            # ジョーカーあり かつ その他のマークが同じ
            # ジョーカーなし かつ すべて同じマーク
        isFlush = \
            [ suit_list.count(suit) for suit in suit_list ].count(4) == 4 if isJokerExists \
            else suit_list.count(suit_list[0]) == 5

        # ロイヤルフラグ
            # ジョーカーあり かつ 数字が [10, J, Q, K, A] のうち4つ揃っている
            # ジョーカーなし かつ 数字が [10, J, Q, K, A]
        isRoyal = \
            set(rank_list) in [ {0, 11, 12, 13, 1}, {10, 0, 12, 13, 1}, {10, 11, 0, 13, 1}, {10, 11, 12, 0, 1}, {10, 11, 12, 13, 0} ] if isJokerExists \
            else rank_list == [1, 10, 11, 12, 13]

        # ストレートフラグ
            # ジョーカーあり かつ 数字集合が連続+ジョーカーの部分集合
            # ジョーカーなし かつ 数字が連続
        isStraght = \
            rank_set <= {0,  2,  3,  4,  5,  6} or \
            rank_set <= {0,  3,  4,  5,  6,  7} or \
            rank_set <= {0,  4,  5,  6,  7,  8} or \
            rank_set <= {0,  5,  6,  7,  8,  9} or \
            rank_set <= {0,  6,  7,  8,  9, 10} or \
            rank_set <= {0,  7,  8,  9, 10, 11} or \
            rank_set <= {0,  8,  9, 10, 11, 12} or \
            rank_set <= {0,  9, 10, 11, 12, 13} or \
            rank_set <= {0, 10, 11, 12, 13,  1} \
            # if isJokerExists \
            # else rank_list[0] + 1 == rank_list[1] \
            # and rank_list[1] + 1 == rank_list[2] \
            # and rank_list[2] + 1 == rank_list[3] \
            # and rank_list[3] + 1 == rank_list[4]

        # print('isFlush: ' + str(isFlush), 'isRoyal: ' + str(isRoyal), 'isStraght: ' + str(isStraght), sep=' | ')

        if isRoyal and isFlush:
            return 'RoyalFlush'

        if isStraght and isFlush:
            return 'StraightFlush'

        if not (isRoyal or isStraght) and isFlush:
            return 'Flush'

        if isRoyal or isStraght:
            return 'Straight'

        if not (isRoyal or isStraght or isFlush) and not isJokerExists:
            return 'NoPair'

        # ジョーカーなしのときはOnePairは rank_set_size < 5 になるためif文の★で処理
        # ★ ジョーカーあり かつ カードの種類が5 ['♦ 3', '🃏 0', '♠ 11', '♥ 4', '♦ 1']
        if isJokerExists:
            return 'OnePair'






# 関数化してfor文でテストデータを検証する
test_data = [
    # ジョーカーなしの手札
    ([ Card(Suit.SPADE, Rank.R10), Card(Suit.SPADE, Rank.JACK), Card(Suit.SPADE, Rank.QUEEN), Card(Suit.SPADE, Rank.KING), Card(Suit.SPADE, Rank.ACE) ],
    'RoyalFlush'),
    ([ Card(Suit.HEART, Rank.R3), Card(Suit.HEART, Rank.R4), Card(Suit.HEART, Rank.R5), Card(Suit.HEART, Rank.R6), Card(Suit.HEART, Rank.R7) ],
    'StraightFlush'),
    ([ Card(Suit.SPADE, Rank.R8), Card(Suit.HEART, Rank.R8), Card(Suit.DIAMOND, Rank.R8), Card(Suit.CLUB, Rank.R8), Card(Suit.DIAMOND, Rank.R2) ],
    'FourCard'),
    ([ Card(Suit.SPADE, Rank.R6), Card(Suit.HEART, Rank.R6), Card(Suit.CLUB, Rank.R6), Card(Suit.DIAMOND, Rank.R3), Card(Suit.CLUB, Rank.R3) ],
    'FullHouse'),
    ([ Card(Suit.CLUB, Rank.KING), Card(Suit.CLUB, Rank.R10), Card(Suit.CLUB, Rank.R8), Card(Suit.CLUB, Rank.R5), Card(Suit.CLUB, Rank.R2) ],
    'Flush'),
    ([ Card(Suit.SPADE, Rank.R5), Card(Suit.DIAMOND, Rank.R6), Card(Suit.DIAMOND, Rank.R7), Card(Suit.HEART, Rank.R8), Card(Suit.CLUB, Rank.R9) ],
    'Straight'),
    ([ Card(Suit.SPADE, Rank.R9), Card(Suit.HEART, Rank.R9), Card(Suit.DIAMOND, Rank.R9), Card(Suit.SPADE, Rank.QUEEN), Card(Suit.CLUB, Rank.R7) ],
    'ThreeCard'),
    ([ Card(Suit.HEART, Rank.QUEEN), Card(Suit.CLUB, Rank.QUEEN), Card(Suit.HEART, Rank.R2), Card(Suit.DIAMOND, Rank.R2), Card(Suit.CLUB, Rank.R7) ],
    'TwoPair'),
    ([ Card(Suit.DIAMOND, Rank.R3), Card(Suit.CLUB, Rank.R3), Card(Suit.SPADE, Rank.JACK), Card(Suit.HEART, Rank.R4), Card(Suit.DIAMOND, Rank.ACE) ],
    'OnePair'),
    ([ Card(Suit.HEART, Rank.R9), Card(Suit.CLUB, Rank.QUEEN), Card(Suit.SPADE, Rank.R8), Card(Suit.DIAMOND, Rank.R5), Card(Suit.CLUB, Rank.R2) ],
    'NoPair'),

    # ジョーカーありの手札
    ([ Card(Suit.SPADE, Rank.R10), Card(Suit.SPADE, Rank.JACK), Card(Suit.SPADE, Rank.QUEEN), Card(Suit.SPADE, Rank.KING), Card(Suit.JOKER, Rank.JOKER) ],
    'RoyalFlush'),
    ([ Card(Suit.HEART, Rank.R3), Card(Suit.HEART, Rank.R4), Card(Suit.JOKER, Rank.JOKER), Card(Suit.HEART, Rank.R6), Card(Suit.HEART, Rank.R7) ],
    'StraightFlush'),
    ([ Card(Suit.SPADE, Rank.R8), Card(Suit.JOKER, Rank.JOKER), Card(Suit.DIAMOND, Rank.R8), Card(Suit.CLUB, Rank.R8), Card(Suit.DIAMOND, Rank.R2) ],
    'FourCard'),
    ([ Card(Suit.JOKER, Rank.JOKER), Card(Suit.HEART, Rank.R6), Card(Suit.CLUB, Rank.R6), Card(Suit.DIAMOND, Rank.R3), Card(Suit.CLUB, Rank.R3) ],
    'FullHouse'),
    ([ Card(Suit.CLUB, Rank.KING), Card(Suit.CLUB, Rank.R10), Card(Suit.CLUB, Rank.R8), Card(Suit.JOKER, Rank.JOKER), Card(Suit.CLUB, Rank.R2) ],
    'Flush'),
    ([ Card(Suit.JOKER, Rank.JOKER), Card(Suit.DIAMOND, Rank.R6), Card(Suit.DIAMOND, Rank.R7), Card(Suit.HEART, Rank.R8), Card(Suit.CLUB, Rank.R9) ],
    'Straight'),
    ([ Card(Suit.SPADE, Rank.R9), Card(Suit.JOKER, Rank.JOKER), Card(Suit.DIAMOND, Rank.R9), Card(Suit.SPADE, Rank.QUEEN), Card(Suit.CLUB, Rank.R7) ],
    'ThreeCard'),
    # ジョーカーありでTwoPairはない
    # ジョーカーありのルールだとそういうつまらないことが起こるのか
    # ([ Card(Suit.HEART, Rank.QUEEN), Card(Suit.CLUB, Rank.QUEEN), Card(Suit.HEART, Rank.R2), Card(Suit.DIAMOND, Rank.R2), Card(Suit.CLUB, Rank.R7) ],
    # 'TwoPair'),
    ([ Card(Suit.DIAMOND, Rank.R3), Card(Suit.JOKER, Rank.JOKER), Card(Suit.SPADE, Rank.JACK), Card(Suit.HEART, Rank.R4), Card(Suit.DIAMOND, Rank.ACE) ],
    'OnePair'),
    # ジョーカーありでNoPairはない
    # ([ Card(Suit.HEART, Rank.R9), Card(Suit.CLUB, Rank.QUEEN), Card(Suit.SPADE, Rank.R8), Card(Suit.DIAMOND, Rank.R5), Card(Suit.CLUB, Rank.R2) ],
    # 'NoPair'),

    # 判定ミスしそうな手札
    ([ Card(Suit.SPADE, Rank.R10), Card(Suit.HEART, Rank.JACK), Card(Suit.DIAMOND, Rank.QUEEN), Card(Suit.CLUB, Rank.KING), Card(Suit.SPADE, Rank.ACE) ],
    'Straight'),
    # トランプの範囲外の数値を入力
    ([ Card(Suit.SPADE, 100), Card(Suit.HEART, Rank.JACK), Card(Suit.DIAMOND, Rank.QUEEN), Card(Suit.CLUB, Rank.KING), Card(Suit.SPADE, Rank.ACE) ],
    'Straight'),
]


start_time = datetime.datetime.now()

for hand, answer in test_data:
    # 手役を判定
    # determined_hand = determine_hand1(hand)
    determined_hand = determine_hand2(hand)

    # 判定結果の真偽
    result = determined_hand == answer
    # 表示用手札
    visual_hand = [str(card) for card in hand]

    print(f'{str(result):5s} | {str(visual_hand):40s} | {determined_hand:>13s} == {answer}')
    # print(result, str(visual_hand), determined_hand, '==', answer)

end_time = datetime.datetime.now()
# テストにかかった時間(秒)
print((end_time - start_time).microseconds / 1000.0)


# print(repr(Card(Suit.SPADE, Rank.R10)))
# print(Rank.ACE)
# print(Rank.TWO)
# print(Rank.KING)
# print(Rank.JOKER)
# print(Rank._1)
# print(str(Suit.CLUB))



# 工夫点
# - Enum型を使って、入力時の安全度や管理のしやすさを強化
# - Flag変数を条件分岐の外に出してif文のネストを2階層までに抑えた
# - ストレートの判定を集合を用いて簡潔に記述

# 反省
# - 最初から綺麗に書こうとし過ぎたので、雑に書いてから共通化を検討してもよかった
# - 80%→100%にするのに時間を使ってしまった 80%できたら次のころやろう

# Rankについては数字で入力した方が可読性は高い
# test_data = [
#     # ジョーカーなしの手札
#     ([ Card(Suit.SPADE, 10), Card(Suit.SPADE, 11), Card(Suit.SPADE, 12), Card(Suit.SPADE, 13), Card(Suit.SPADE, 1) ],
#     'RoyalFlush'),
#     ([ Card(Suit.HEART, 3), Card(Suit.HEART, 4), Card(Suit.HEART, 5), Card(Suit.HEART, 6), Card(Suit.HEART, 7) ],
#     'StraightFlush'),
#     ([ Card(Suit.SPADE, 8), Card(Suit.HEART, 8), Card(Suit.DIAMOND, 8), Card(Suit.CLUB, 8), Card(Suit.DIAMOND, 2) ],
#     'FourCard'),
#     ([ Card(Suit.SPADE, 6), Card(Suit.HEART, 6), Card(Suit.CLUB, 6), Card(Suit.DIAMOND, 3), Card(Suit.CLUB, 3) ],
#     'FullHouse'),
#     ([ Card(Suit.CLUB, 13), Card(Suit.CLUB, 10), Card(Suit.CLUB, 8), Card(Suit.CLUB, 5), Card(Suit.CLUB, 2) ],
#     'Flush'),
#     ([ Card(Suit.SPADE, 5), Card(Suit.DIAMOND, 6), Card(Suit.DIAMOND, 7), Card(Suit.HEART, 8), Card(Suit.CLUB, 9) ],
#     'Straight'),
#     ([ Card(Suit.SPADE, 9), Card(Suit.HEART, 9), Card(Suit.DIAMOND, 9), Card(Suit.SPADE, 12), Card(Suit.CLUB, 7) ],
#     'ThreeCard'),
#     ([ Card(Suit.HEART, 12), Card(Suit.CLUB, 12), Card(Suit.HEART, 2), Card(Suit.DIAMOND, 2), Card(Suit.CLUB, 7) ],
#     'TwoPair'),
#     ([ Card(Suit.DIAMOND, 3), Card(Suit.CLUB, 3), Card(Suit.SPADE, 11), Card(Suit.HEART, 4), Card(Suit.DIAMOND, 1) ],
#     'OnePair'),
#     ([ Card(Suit.HEART, 9), Card(Suit.CLUB, 12), Card(Suit.SPADE, 8), Card(Suit.DIAMOND, 5), Card(Suit.CLUB, 2) ],
#     'NoPair'),

#     # ジョーカーありの手札
#     ([ Card(Suit.SPADE, 10), Card(Suit.SPADE, 11), Card(Suit.SPADE, 12), Card(Suit.SPADE, 13), Card(Suit.JOKER, 0) ],
#     'RoyalFlush'),
#     ([ Card(Suit.HEART, 3), Card(Suit.HEART, 4), Card(Suit.JOKER, 0), Card(Suit.HEART, 6), Card(Suit.HEART, 7) ],
#     'StraightFlush'),
#     ([ Card(Suit.SPADE, 8), Card(Suit.JOKER, 0), Card(Suit.DIAMOND, 8), Card(Suit.CLUB, 8), Card(Suit.DIAMOND, 2) ],
#     'FourCard'),
#     ([ Card(Suit.JOKER, 0), Card(Suit.HEART, 6), Card(Suit.CLUB, 6), Card(Suit.DIAMOND, 3), Card(Suit.CLUB, 3) ],
#     'FullHouse'),
#     ([ Card(Suit.CLUB, 13), Card(Suit.CLUB, 10), Card(Suit.CLUB, 8), Card(Suit.JOKER, 0), Card(Suit.CLUB, 2) ],
#     'Flush'),
#     ([ Card(Suit.JOKER, 0), Card(Suit.DIAMOND, 6), Card(Suit.DIAMOND, 7), Card(Suit.HEART, 8), Card(Suit.CLUB, 9) ],
#     'Straight'),
#     ([ Card(Suit.SPADE, 9), Card(Suit.JOKER, 0), Card(Suit.DIAMOND, 9), Card(Suit.SPADE, 12), Card(Suit.CLUB, 7) ],
#     'ThreeCard'),
#     # ジョーカーありでTwoPairはない
#     # ジョーカーありのルールだとそういうつまらないことが起こるのか
#     # ([ Card(Suit.HEART, 12), Card(Suit.CLUB, 12), Card(Suit.HEART, 2), Card(Suit.DIAMOND, 2), Card(Suit.CLUB, 7) ],
#     # 'TwoPair'),
#     ([ Card(Suit.DIAMOND, 3), Card(Suit.JOKER, 0), Card(Suit.SPADE, 11), Card(Suit.HEART, 4), Card(Suit.DIAMOND, 1) ],
#     'OnePair'),
#     # ジョーカーありでNoPairはない
#     # ([ Card(Suit.HEART, 9), Card(Suit.CLUB, 12), Card(Suit.SPADE, 8), Card(Suit.DIAMOND, 5), Card(Suit.CLUB, 2) ],
#     # 'NoPair'),

#     # 判定ミスしそうな手札
#     ([ Card(Suit.SPADE, 10), Card(Suit.HEART, 11), Card(Suit.DIAMOND, 12), Card(Suit.CLUB, 13), Card(Suit.SPADE, 1) ],
#     'Straight'),
#     # トランプの範囲外の数値を入力
#     ([ Card(Suit.SPADE, 100), Card(Suit.HEART, 11), Card(Suit.DIAMOND, 12), Card(Suit.CLUB, 13), Card(Suit.SPADE, 1) ],
#     'Straight'),
# ]
