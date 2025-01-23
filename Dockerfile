# Python 3.9 slim 이미지를 베이스로 사용
FROM python:3.9-slim

# 작업 디렉터리 설정
WORKDIR /app

# requirements.txt를 컨테이너에 복사하고 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 전체 소스코드 복사
COPY . .

# 컨테이너 포트 노출
EXPOSE 5000

# 앱 실행
CMD ["python", "app.py"]
