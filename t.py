# サンプルリスト
sample_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# スタートとエンドのインデックス
i = 3  # 開始インデックス
n = 7  # 終了インデックス（このインデックスの要素は含まれない）

# i 番目から n 番目までの要素でループを回す内包表記
sliced_list = [element for element in sample_list[i:n]]

print(sliced_list)