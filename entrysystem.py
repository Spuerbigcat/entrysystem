import threading
from playsound import playsound
import nfc
import time
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# サービスコード（学籍番号が含まれる領域を指定）
service_code = XXXXXX

# 大学の学科対応表
university_departments = {
    "01": "経済学科",
    "02": "経営学科",
    "03": "社会学科",
    "04": "商学科",
}

# 短大の学科対応表
junior_college_departments = {
    "11": "学科",
    "12": "学科",
    "13": "学科",
}

# 大学院の研究科対応表
graduate_school_departments = {
    "21": "国際研究科",
    "22": "心理学研究科",
    "23": "経営学研究科",
}

# 入退室管理辞書
attendance = {}

# Google Sheets API の初期化
def init_google_sheets():
    SERVICE_ACCOUNT_FILE = "C:/Users/hogehoge/hogehoge.json"
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    try:
        credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        client = gspread.authorize(credentials)
        spreadsheet_id = "hogehogehogehogeohoge"
        sheet = client.open_by_key(spreadsheet_id)
        print("スプレッドシートに接続成功")
        return sheet
    except Exception as e:
        print(f"Google Sheets API の初期化に失敗しました: {e}")
        return None

# スプレッドシートに記録
def log_attendance_to_sheets(sheet, gakuban, user_type, department, identifier, status, current_time):
    try:
        worksheet = sheet.worksheet("hoge")
        date, time_ = current_time.split(" ")  # 日付と時刻を分割
        log_data = [gakuban, user_type, department, identifier, status, date, time_]
        worksheet.append_row(log_data, value_input_option="USER_ENTERED")
        print("スプレッドシートに記録が完了しました。")
    except gspread.exceptions.WorksheetNotFound:
        print("シート 'MORI' が見つかりません。新規作成します...")
        worksheet = sheet.add_worksheet(title="MORI", rows=100, cols=10)
        worksheet.append_row(["学籍番号", "種別", "学科", "出席番号", "状態", "日付", "時刻"])
        log_data = [gakuban, user_type, department, identifier, status, date, time_]
        worksheet.append_row(log_data, value_input_option="USER_ENTERED")
    except Exception as e:
        print(f"スプレッドシートへの記録中にエラーが発生しました: {e}")

def play_sound(sound_type):
    """音声を再生する"""
    try:
        playsound(r"C:\hogehoge\hogehoge\tuuti.mp3")
    except Exception as e:
        print(f"音声再生中にエラーが発生しました: {e}")

def get_department_from_gakuban(gakuban):
    """学籍番号から学科・研究科を判別"""
    if len(gakuban) < 10:
        return "不明", "不明", "不明"
    
    year = gakuban[1:5]
    department_code = gakuban[5:7]
    student_number = gakuban[7:]

    if department_code in university_departments:
        return "大学", university_departments[department_code], student_number
    elif department_code in junior_college_departments:
        return "短大", junior_college_departments[department_code], student_number
    elif department_code in graduate_school_departments:
        return "大学院", graduate_school_departments[department_code], student_number
    else:
        return "不明", "不明", "不明"

def identify_user(gakuban):
    """学籍番号から学生か教員を判別"""
    if gakuban.startswith("XXXXXXXXXXXX"):
        teacher_number = gakuban[hoge:]
        return "教員", "-", teacher_number
    else:
        return get_department_from_gakuban(gakuban)

# スプレッドシートの初期化
sheet = init_google_sheets()

# 再読み取り制限のための変数
recent_idm = None
recent_timestamp = 0
cooldown_seconds = 5  # 3秒間は同じカードを再読み取りしない

# NFC タグを検出した際の処理
def connected(tag):
    global recent_idm, recent_timestamp

    print("カード検出")
    try:
        idm = tag.identifier.hex()
        current_time = time.time()

        # 再読み取り制限を適用
        if idm == recent_idm and (current_time - recent_timestamp) < cooldown_seconds:
            print("少し時間を空けてから再度タッチしてください。")
            return

        # IDmと時刻を更新
        recent_idm = idm
        recent_timestamp = current_time

        sc = nfc.tag.tt3.ServiceCode(service_code >> 6, service_code & hoge)
        bc = nfc.tag.tt3.BlockCode(0, service=0)
        if isinstance(tag, nfc.tag.tt3.Type3Tag):
            feli_data = tag.read_without_encryption([sc], [bc])
            gakuban = feli_data[:10].decode('utf-8')
            user_type, department, identifier = identify_user(gakuban)
            handle_attendance(gakuban, user_type, department, identifier)
        else:
            print("学生証が読み取れません")
    except Exception as e:
        print(f"NFC 読み取りエラー: {e}")

def handle_attendance(gakuban, user_type, department, identifier):
    """入退室を管理し、結果を表示"""
    global attendance
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if gakuban in attendance:
        if attendance[gakuban]['status'] == '入室':
            attendance[gakuban] = {'status': '退室', 'time': current_time}
            status = "退室"
            play_sound("exit")  # 退室時の音声を再生
        else:
            attendance[gakuban] = {'status': '入室', 'time': current_time}
            status = "入室"
            play_sound("entry")  # 入室時の音声を再生
    else:
        attendance[gakuban] = {'status': '入室', 'time': current_time}
        status = "入室"
        play_sound("entry")  # 入室時の音声を再生

    # 結果を出力
    print(f"{gakuban} ({user_type} - 学科: {department}, 出席番号: {identifier}) が{status}しました。時刻: {current_time}")
    log_attendance_to_sheets(sheet, gakuban, user_type, department, identifier, status, current_time)

# 入退室リセット処理
def reset_attendance():
    """9時20分と21時20分に入室状態をリセットする"""
    global attendance
    while True:
        now = datetime.now()
        # 9時20分または21時20分のタイミングでリセット
        if (now.hour == 9 and now.minute == 20) or (now.hour == 21 and now.minute == 20):
            print(f"リセット処理を開始しました ({now.strftime('%Y-%m-%d %H:%M:%S')})")
            for gakuban, record in list(attendance.items()):
                if record['status'] == '入室':
                    # 強制的に退室
                    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                    user_type, department, identifier = identify_user(gakuban)
                    attendance[gakuban]['status'] = '退室'
                    attendance[gakuban]['time'] = current_time
                    log_attendance_to_sheets(sheet, gakuban, user_type, department, identifier, "退室", current_time)
                    print(f"{gakuban} が強制退室されました。")
            print("リセット処理が完了しました。")
            # リセット処理後に1分間スリープして重複実行を防ぐ
            time.sleep(60)
        time.sleep(1)

# リセットスレッドを開始
reset_thread = threading.Thread(target=reset_attendance, daemon=True)
reset_thread.start()


# NFC読み取りループ
while True:
    with nfc.ContactlessFrontend('usb') as m:
        m.connect(rdwr={'on-connect': connected})
        time.sleep(1)
