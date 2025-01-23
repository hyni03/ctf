from flask import Blueprint, request, redirect, url_for, render_template
from utils.jwt import verify_token
from flask import current_app



admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/admin-panel")
def admin_panel():
    token = request.cookies.get("token")
    if not token:
        return redirect(url_for("auth_bp.login"))
    
    payload = verify_token(token)
    if not payload:
        return "토큰이 유효하지 않습니다.", 401

    # JWT 내 role 값 확인 (관리자여야 접근 가능)
    if payload.get("role") != "admin":
        return "관리자 계정이 아닙니다.", 403

    # 관리자 페이지에서 FLAG 출력
    return render_template("admin.html", flag=current_app.config['FLAG'])
