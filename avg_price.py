from google_sheets_manager import GoogleSheetsManager


def read_avg_price():
    # 스프레드시트 상수 정의
    SPREADSHEET_ID = "1KwBg0x39gaaKjWFEt--tlQuX8mAb5pL6ZWtXMEI9VCs"
    RANGE_NAME = "USDT!A3:B4"

    # GoogleSheetsManager 인스턴스 생성
    sheets_manager = GoogleSheetsManager()

    # 데이터 읽기 예제
    data = sheets_manager.read_range(SPREADSHEET_ID, RANGE_NAME)

    return data[0][1], data[1][1]
