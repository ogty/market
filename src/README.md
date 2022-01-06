# Component

### ファイルの説明

 - `analizer` : 業種・市場を分析
 - `bollinger_band_counter` : 複数銘柄の最新の終値のボリンジャーバンドを集計
 - `code_acqusition` :  選択したカテゴリーの全てのコードを取得
 - `dataframe_slicer` : DataFrameを任意の数に分ける
 - `download_update` : 最新の上場銘柄一覧をダウンロード
 - `generate_schedule` : スケジュールを作成
 - `historical_volatirity` : ヒストリカルボラティリティを計算
 - `loading` : ローディングを実装
 - `market_data_acquisition` : `code_acqusition`の拡張版で、コードだけでなく価格や出来高を取得
 - `market_trend` : 市場のトレンド取得、営業日判定、Twitter・Slackボット
 - `stock_data_acquisition` : 任意の銘柄の始値や終値などを取得
 - `text_length_counter` : 全角・半角の長さを取得
 - `totalling` : 市場を集計

***

### `generate_schedule`

指定した間隔でスケジュールを作成できます。

#### 引数について

 - `fill(True)`：`0`で埋めるかどうかを指定できます。
 - `addition`：時間を追加できます。「`'09:05'`, `'9:5'`」のどちらでも指定可能です。
 - `delete`：関数によって生成された時間の中で、必要のない時間をあらかじめ選択できます。
 - `step(30)`：分の間隔を指定できます。`1～59`までの値を取ります。
 - `delimiter(':')`：時間と分を区切る文字を指定できます。ここに空の文字列を入れることはできません。
 - `include(True)`：ここを`False`にした場合は`range(9, 15)`としたときの15が追加されません。

##### ※カッコの中はデフォルトの値を示しています。

```python
>>> generate_schedule(range(9, 12), step=20)
['09:00', '09:20', '09:40', '10:00', '10:20', '10:40', '11:00', '11:20', '11:40', '12:00']

>>> generate_schedule(range(8, 10), fill=False, include=False)
['8:0', '8:30', '9:0', '9:30']

>>> generate_schedule(range(9, 11), addition=['09:05'])
['09:00', '09:05', '09:30', '10:00', '10:30', '11:00']

>>> generate_schedule(range(9, 15), delete=['11:30', '12:00', '12:30'])
['09:00', '09:30', '10:00', '10:30', '11:00', '13:00', '13:30', '14:00', '14:30', '15:00']

>>> generate_schedule(range(3, 6), delimiter="-")
['03-00', '03-30', '04-00', '04-30', '05-00', '05-30', '06-00']
```

***

### `totalling`

`totalling`を実行することで、以下の画像とテキストデータを取得できる。
`Range`は階級を表しており、「`Rate`, `Price`, `Vollume`」はそれぞれの階級における中央値を表す。
`Market`は階級の中で一番多く割合を占めていた市場の名称と、その割合を示す。

![totalling sample image](../data/images/totalling_sample.png)

```
2022/01/04
    
UP
≡≡≡≡≡
    Range    |  Rate  |  Price  |  Volume  |     Market     
============================================================
    1 ~  100 |   6.42 |  1104.5 |  79350.0 | 東証JQS ( 32%)
  101 ~  200 |   3.58 |   933.0 |  26600.0 |    〃   ( 36%)
  201 ~  300 |   2.63 |   932.0 |  19800.0 |    〃   ( 28%)
  301 ~  400 |    2.1 |  1080.5 |  17150.0 | 東証1部 ( 36%)
  401 ~  500 |   1.73 |  1094.5 |  22300.0 |    〃   ( 41%)
  501 ~  600 |   1.47 |  1253.5 |  14050.0 |    〃   ( 32%)
  601 ~  700 |   1.24 |  1203.0 |   9500.0 |    〃   ( 45%)
  701 ~  800 |   1.05 |   976.5 |  10550.0 |    〃   ( 37%)
  801 ~  900 |   0.89 |  1058.5 |  12400.0 |    〃   ( 41%)
  901 ~ 1000 |   0.75 |  1234.0 |  25300.0 |    〃   ( 51%)
 1001 ~ 1100 |   0.64 |  1323.0 |  14050.0 |    〃   ( 54%)
 1101 ~ 1200 |   0.54 |  1357.0 |  17150.0 |    〃   ( 50%)
 1201 ~ 1300 |   0.47 |  1144.5 |  12050.0 |    〃   ( 48%)
 1301 ~ 1400 |   0.36 |  1144.5 |  29950.0 |    〃   ( 56%)
 1401 ~ 1500 |    0.3 |  1337.5 |  14150.0 |    〃   ( 46%)
 1501 ~ 1600 |   0.21 |  1627.0 |   9900.0 |    〃   ( 52%)
 1601 ~ 1700 |   0.13 |  1972.5 |  10400.0 |    〃   ( 53%)
 1701 ~ 1800 |   0.07 |  1670.5 |  18300.0 |    〃   ( 50%)

DOWN
≡≡≡≡≡≡
    Range    |  Rate  |  Price  |  Volume  |     Market     
============================================================
    1 ~  100 |  -0.08 |  2009.5 |  26557.5 | 東証1部 ( 66%)
  101 ~  200 |  -0.14 |  1570.0 |  10876.0 |    〃   ( 58%)
  201 ~  300 |   -0.2 |  1385.0 |  29900.0 |    〃   ( 54%)
  301 ~  400 |  -0.29 |  2283.0 |  15700.0 |    〃   ( 54%)
  401 ~  500 |  -0.36 |  1815.0 |  18150.0 |    〃   ( 56%)
  501 ~  600 |  -0.41 |  1550.0 |  24250.0 |    〃   ( 68%)
  601 ~  700 |  -0.49 |  1775.5 |  20250.0 |    〃   ( 63%)
  701 ~  800 |  -0.55 |  1639.0 |  25700.0 |    〃   ( 60%)
  801 ~  900 |  -0.62 |  1684.5 |  33700.0 |    〃   ( 69%)
  901 ~ 1000 |   -0.7 |  1263.0 |  42100.0 |    〃   ( 70%)
 1001 ~ 1100 |  -0.79 |  1524.5 |  51950.0 |    〃   ( 82%)
 1101 ~ 1200 |  -0.88 |  1598.0 |  59050.0 |    〃   ( 75%)
 1201 ~ 1300 |  -0.98 |  1850.5 |  31850.0 |    〃   ( 76%)
 1301 ~ 1400 |  -1.08 |  1323.0 |  25400.0 |    〃   ( 65%)
 1401 ~ 1500 |  -1.22 |  1377.0 |  45000.0 |    〃   ( 74%)
 1501 ~ 1600 |  -1.36 |  1507.5 |  62000.0 |    〃   ( 70%)
 1601 ~ 1700 |  -1.52 |  1676.0 |  29500.0 |    〃   ( 72%)
 1701 ~ 1800 |  -1.75 |  1292.0 |  47250.0 |    〃   ( 64%)
 1801 ~ 1900 |  -2.09 |  1445.0 |  40200.0 |    〃   ( 55%)
 1901 ~ 2000 |   -2.7 |  1432.0 |  48650.0 |    〃   ( 51%)
 2001 ~ 2100 |   -4.4 |  1405.0 | 123500.0 | マザーズ( 43%)
 2101 ~ 2200 | -21.43 |  1029.0 | 672450.0 |    〃   (100%)
```

***

### `historical_volatirity`

![hv](../data/images/historical_volatility.png)