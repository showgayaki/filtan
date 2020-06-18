# filtan
![filtan](https://user-images.githubusercontent.com/47170845/84984634-3617ad00-b176-11ea-84b9-7fea38ce56d6.png)
## 準備
### pipenv
`pip install pipenv`  
で、PCにpipenvをインストールしておく。

### filtan
filtanをダウンロード、解凍して「token」フォルダを作成する。

 ![token](https://user-images.githubusercontent.com/47170845/84983633-1ed7c000-b174-11ea-9ec3-6e7b7a7592b7.png)

### Gmail API
[このあたり](https://qiita.com/muuuuuwa/items/822c6cffedb9b3c27e21)を参考にGmail APIを利用できるようにする。  
追加するスコープは下記。
- https://mail.google.com/
- https://www.googleapis.com/auth/gmail.labels
- https://www.googleapis.com/auth/gmail.modify
- https://www.googleapis.com/auth/gmail.settings.basic

できたら、client_id.jsonをダウンロードして作成した「token」フォルダに保存する。

## インストール
「install.bat」を実行。

## 実行
「build\exe.～～」フォルダにfitan.exeができているのでこれを実行すればOK。
![filtan_exe](https://user-images.githubusercontent.com/47170845/84984384-aa9e1c00-b175-11ea-8b33-0cad567c635b.png)

デスクトップにショートカットを作成するなど、お好みで。

## デモ
### ラベルのみ作成
![label](https://user-images.githubusercontent.com/47170845/84985156-35cbe180-b177-11ea-9a11-32153b1bd483.gif)

### ラベルとフィルター作成
![filter](https://user-images.githubusercontent.com/47170845/84985778-5b0d1f80-b178-11ea-8b9a-70f7c93fc350.gif)
既存ラベルへのフィルター作成も可。