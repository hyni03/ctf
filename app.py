from flask import Flask, render_template
from config import Config
from routes.auth import auth_bp
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # index.html 을 렌더링하는 기본 루트 추가
    @app.route("/")
    def index():
        return render_template("index.html")

    # 블루프린트 등록
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)