import mysql.connector
from datetime import datetime

# MySQL 연결 설정
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1111",
  database="capstone"
)

# 커서 생성
cursor = mydb.cursor()

# 서버 클래스 내의 ClientThread 클래스에서 수신한 메시지를 MySQL에 저장하는 함수
def save_to_database(event, hash,  message):
    try:
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # SQL 쿼리 실행
        sql = 'INSERT INTO log (event, create_date, hash, message) VALUES ("{0}", "{1}", "{2}", "{3}")'.format(event, current_datetime, hash, message)
        cursor.execute(sql)

        # 변경사항 커밋
        mydb.commit()

        print("데이터가 성공적으로 저장되었습니다.")
    except Exception as e:
        print("데이터 저장 중 오류 발생:", e)


