import json
import base64
from flask import Blueprint, request, redirect, url_for, render_template, make_response, jsonify
from datetime import datetime

from utils.jwt import generate_token, verify_token, pad_base64

# 블루프린트 생성
auth_bp = Blueprint("auth_bp", __name__)

# 단순 사용자 DB (CTF에서는 관리자 계정과 일반 계정을 구분)
USERS = {
    "testuser@test.com": {"password": "password123", "role": "user", "user_id": 1001},
    "admin@shop.com": {"password": "adminpass", "role": "admin", "user_id": 1}
}

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    # POST: 이메일, 비밀번호 검증
    email = request.form.get("email")
    password = request.form.get("password")
    user = USERS.get(email)

    if not user or user["password"] != password:
        return "잘못된 이메일 혹은 비밀번호입니다.", 401

    token = generate_token(user)
    response = make_response(redirect(url_for("admin_bp.admin_panel")))
    # 쿠키에 토큰 저장 (실제 운영환경에서는 HttpOnly/secure 적용 필요)
    response.set_cookie("token", token)
    return response

@auth_bp.route("/debug-token", methods=["GET"])
def debug_token():
    # 힌트용 : 쿠키에 저장된 JWT의 Header와 Payload를 Base64 디코딩하여 확인.
    token = request.cookies.get("token")
    if not token:
        return "토큰이 없습니다.", 400

    try:
        header_enc, payload_enc, signature = token.split(".")
        header = json.loads(base64.urlsafe_b64decode(pad_base64(header_enc)).decode())
        payload = json.loads(base64.urlsafe_b64decode(pad_base64(payload_enc)).decode())
        return jsonify({"header": header, "payload": payload, "signature": signature})
    except Exception as e:
        return str(e), 500
