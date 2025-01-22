import base64
import json
from datetime import datetime, timedelta
import jwt
from flask import current_app

def generate_token(user):
    # 사용자 정보를 기반으로 JWT 생성.
    payload = {
        "user_id": user["user_id"],
        "role": user["role"],
        "exp": datetime.utcnow() + current_app.config.get("JWT_EXP_DELTA", timedelta(minutes=30))
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
    return token

def verify_token(token):
    try:
        # 토큰의 헤더를 먼저 확인하여 "alg" 값 가져옴옴
        header_enc = token.split('.')[0]
        header_json = base64.urlsafe_b64decode(pad_base64(header_enc)).decode()
        header = json.loads(header_json)
        alg = header.get("alg", "HS256")  # 기본적으로 HS256으로 가정

        if alg.lower() == "none":
            # alg가 'none'인 경우, 서명 검증을 건너뛰고 Payload 디코딩
            payload = jwt.decode(token, options={"verify_signature": False})
        else:
            # 그렇지 않으면 올바른 서명 검증 수행 (payload 변조 시 InvalidSignatureError 발생)
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return payload

    except Exception as e:
        print("토큰 검증 오류:", e)
        return None

def pad_base64(b64_string):
    # Base64 디코딩을 위해 '=' 패딩 추가 함수
    return b64_string + "=" * (-len(b64_string) % 4)
