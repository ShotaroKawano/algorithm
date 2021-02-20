#set #集合 #検証 #単体テスト


# coding: utf-8

# 手役を判定するプログラム
# A から Z のアルファベット、あるいは、 「*」 が書かれたカードが４枚配られ手役を作る
# ("FourCard" ＞ "ThreeCard" ＞ "TwoPair" ＞ "OnePair" ＞ "NoPair")
# 与えられる文字列は、 高々１つしかワイルドカード * を含みまない

def determine_hand(cards):
    count_list = []
    wildcard_exists = '*' in cards
    cards = cards.replace('*', '')
    # 手札を1枚ずつループ
    for card in cards:
        # 文字の個数をカウントしてリストに追加
        count_list.append(cards.count(card))

    # print(count_list)
    # [2, 2, 1] *を除く

    # *を含む場合、リスト内のカウントを1ずつ増やす
    if wildcard_exists:
        count_list = list(map(lambda x:x+1, count_list))

    # print(count_list)
    # [3, 3, 2] *を除く

    # 手役の辞書
    # TwoPairのみ下記ロジックで判定できないので別ロジックで判定 '2-2':'TwoPair'
    hand_dict = {'1':'NoPair', '2':'OnePair', '3':'ThreeCard', '4':'FourCard'}

    # 先にTwoPairの判定
    if count_list == [2, 2, 2, 2]:
        return 'TwoPair'

    # 最大カウント数で辞書から手役を判定
    hand = hand_dict[str(max(count_list))]
    return hand

# 手札を文字列として取得 ex. ABCD, *ZZD
# cards = input()
# print(determine_hand(cards))

# 関数化してfor文でテストデータを検証する
test_data = {
    'ADZF': 'NoPair',
    'k*LM': 'OnePair',
    'TUZU': 'OnePair',
    'HFHF': 'TwoPair',
    '*SST': 'ThreeCard',
    'KDKK': 'ThreeCard',
    'AAAA': 'FourCard',
    'D*DD': 'FourCard'}
for cards, answer in test_data.items():
    determined_hand = determine_hand(cards)
    print(determined_hand == answer, cards, determined_hand, '==', answer)

# FB
# - setを使うと効率的
# - 処理が面倒な*を最初に取り除くのは有効
# - 5枚に増えた場合の拡張性
# - 次回はポーカー なんならポーカーゲーム作ってもいい reactでやるか？

# ================================================================================
print('===========================================================================')

# coding: utf-8

# 手役を判定するプログラム
# A から Z のアルファベット、あるいは、 「*」 が書かれたカードが４枚配られ手役を作る
# ("FourCard" ＞ "ThreeCard" ＞ "TwoPair" ＞ "OnePair" ＞ "NoPair")
# 与えられる文字列は、 高々１つしかワイルドカード * を含みまない

def determine_hand2(cards):
    wildcard_exists = '*' in cards
    cards = cards.replace('*', '')
    # カードの種類数(setは重複を取り除く)
    set_size = len(set(cards))

    if set_size == 1:
        return 'FourCard'
    elif set_size == 2:
        # 個数が1のカードが存在した場合 ThreeCard
        if 1 in [cards.count(card) for card in cards]:
            return 'ThreeCard'
        else:
            return 'TwoPair'
        # if wildcard_exists:
        #     return 'ThreeCard'
        # else:
        #     # 1番目のカードの個数が2の場合 TwoPair 1か3の場合 ThreeCard
        #     return 'TwoPair' if len(list(filter(lambda card: card == cards[0], cards))) == 2 else 'ThreeCard'
    elif set_size == 3:
        return 'OnePair'
    elif set_size == 4:
        return 'NoPair'
    else:
        return '想定外の手役です'

# 手札を文字列として取得 ex. ABCD, *ZZD
# cards = input()
# print(determine_hand2(cards))

# 関数化してfor文でテストデータを検証する
test_data = {
    'ADZF': 'NoPair',
    'k*LM': 'OnePair',
    'TUZU': 'OnePair',
    'HFHF': 'TwoPair',
    '*SST': 'ThreeCard',
    'KDKK': 'ThreeCard',
    'AAAA': 'FourCard',
    'D*DD': 'FourCard'}
for cards, answer in test_data.items():
    determined_hand = determine_hand2(cards)
    print(determined_hand == answer, cards, determined_hand, '==', answer)
