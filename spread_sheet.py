import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os

# .envファイルから環境変数を読み込む
load_dotenv()
credential_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if credential_path:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path
else:
    raise Exception("GOOGLE_APPLICATION_CREDENTIALS is not set.")

try:
    # サービスアカウントの認証情報を使ってクライアントを作成
    client = gspread.service_account(filename=credential_path)

    # スプレッドシートを名前で開く
    # 'Your Spreadsheet Name' の部分は実際に存在するスプレッドシート名に書き換えてください
    spreadsheet = client.open("mahjong_team.xlsx")

    # 最初のシートを選択
    sheet = spreadsheet.sheet1

    # 動作確認（例：A1セルの値を取得して表示）
    cell_value = sheet.acell('A1').value
    print(f"シート '{sheet.title}' のA1セルの値は: {cell_value}")

except FileNotFoundError:
    print(f"エラー: 認証情報ファイルが見つかりません。パスを確認してください: {credential_path}")
except gspread.exceptions.SpreadsheetNotFound:
    print("エラー: 指定されたスプレッドシートが見つかりません。名前が正しいか、サービスアカウントに共有されているか確認してください。")
except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")