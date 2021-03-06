#正規表現


# coding: utf-8
import re

# *** 変換ルール ***
# 末尾が s, sh, ch, o, x のいずれかである英単語の末尾に es を付ける
# 末尾が f, fe のいずれかである英単語の末尾の f, fe を除き、末尾に ves を付ける
# 末尾の1文字が y で、末尾から2文字目が a, i, u, e, o のいずれでもない英単語の末尾の y を除き、末尾に ies を付ける
# 上のいずれの条件にも当てはまらない英単語の末尾には s を付ける
# ==================================================================================================================
# *** 正規表現tips ***
# r's|sh|ch|o|x$' と r'(s|sh|ch|o|x)$は同じ挙動
# r'.+(s|sh|ch|o|x)$' だと単語全体がマッチする
# [^abc] の^は否定
# match は先頭からマッチしないといけない
# repl は replace という意味

# # 正規表現オブジェクトを生成(少し早くなるかも/複数回呼ぶとき/可読性は悪い)
# re_sshchox = re.compile(r'(s|sh|ch|o|x)$')
# re_ffe = re.compile(r'(f|fe)$')
# re_aiueoy = re.compile(r'[^aiueo]y$')
# re_y = re.compile(r'y$')

# # 複数形に変換
# def pluralize(word):
#     if re_sshchox.search(word):
#         return word + 'es'
#     elif re_ffe.search(word):
#         return re_ffe.sub('', word) + 'ves'
#     elif re_aiueoy.search(word):
#         return re_y.sub('', word) + 'ies'
#     else:
#         return word + 's'

# 複数形に変換
def pluralize(word):
    if re.search(r'(s|sh|ch|o|x)$', word):
        return word + 'es'
    elif re.search(r'(f|fe)$', word):
        return re.sub(r'(f|fe)$', '', word) + 'ves'
    elif re.search(r'[^aiueo]y$', word):
        return re.sub(r'y$', '', word) + 'ies'
    else:
        return word + 's'


# 入力値N
# input_line = input()
# N = int(input_line)
N = int(input())

# 入力値 単語
# words = []
# for i in range(0, N):
#   val = input()
#   if val:
#     words.append(val)

# 入力値 単語
# 空文字列が渡されないならリスト内包表記の方がスッキリ書ける
words = [input() for i in range(N)]
# words = [input() for i in range(0, N)]
# print(words)

# 結果を表示
# if words:
#     for word in words:
#         print(pluralize(word))
for word in words:
    print(pluralize(word))
