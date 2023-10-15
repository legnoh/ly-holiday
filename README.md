# ly-holiday

LINEヤフー株式会社における土日以外の休日をまとめた iCal/JSON、並びにそれらを生成するスクリプトです。

## usage

下記のURLから照会カレンダーとして、各種カレンダーアプリでお使い頂けます。

- 日本の祝日＋特別休日
  - https://lycorp.event.lkj.io/lyj-holidays.ics
  - https://lycorp.event.lkj.io/lyj-holidays.json
- 特別休日のみ（LINE WORKSなど既に祝日表示があるもの向け）
  - https://lycorp.event.lkj.io/ly-holidays.ics
  - https://lycorp.event.lkj.io/ly-holidays.json

## make

```sh
git clone https://github.com/legnoh/ly-holiday.git && cd ly-holiday
curl -LO https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv
pipenv run main
```

## appendix

- LINEヤフー株式会社は、完全週休2日制（土日）、国民の祝日、年末年始（12月29日から1月4日まで）が休日となります。
  - [エンジニア職の募集要項｜新卒採用｜LINEヤフー株式会社](https://www.lycorp.co.jp/ja/recruit/newgrads/engineer/)
- LINEヤフー株式会社は、祝日が土曜日にあたった場合、前労働日を振り替え特別休日とする"ハッピーフライデー（土曜祝日振替休暇）"があります。
  - [働く環境｜LINEヤフー株式会社](https://www.lycorp.co.jp/ja/recruit/workplace/)
- 日本国の祝日の取得に、内閣府の提供するCSVデータを利用しています。
  - [国民の祝日について - 内閣府](https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html) - [CSV](https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv)
