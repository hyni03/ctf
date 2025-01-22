# CTF JWT 취약점 문제 풀이 가이드

이 문제는 JWT 토큰의 `alg` 설정 취약점을 이용하여 일반 사용자 계정으로 관리자 페이지에 접근할 수 있도록 구성된 웹 애플리케이션입니다.

## 문제 개요

- **목표**: 관리자 페이지(`/admin-panel`)에서 FLAG 획득
- **취약점 요약**:  
  - 웹 어플리케이션은 JWT를 사용하여 로그인 상태를 관리합니다.
  - JWT 토큰 발급 시 Header의 `alg` 값은 원래 `"HS256"`으로 지정되어 있으나, 서버는 검증 과정에서 `alg` 값을 `"none"`으로 변경한 토큰에 대한 서명 검증을 우회합니다.
  - Payload에 포함된 `role` 값이 `admin`이어야 관리자 페이지에 접근할 수 있습니다.

## 취약점 분석

1. **JWT 구조 이해**  
   JWT는 Base64 URL-safe 인코딩된 **Header**, **Payload**, **Signature** 세 부분으로 구성되어 있습니다.
   - Header 예시:  
     ```json
     {
       "alg": "HS256",
       "typ": "JWT"
     }
     ```
   - Payload 예시:  
     ```json
     {
       "user_id": 1001,
       "role": "user",
       "exp": 1699999999
     }
     ```

2. **취약점 포인트**  
   - 서버는 JWT 검증 시 `alg` 값으로 `"HS256"`뿐만 아니라 `"none"` 알고리즘을 허용합니다.
   - 이로 인해 공격자는 다음과 같이 토큰을 변조할 수 있습니다.
     - Header의 `alg` 값을 `"none"`으로 수정
     - Payload의 `role` 값을 `"user"`에서 `"admin"`으로 수정
     - 서명(Signature)은 비워둡니다.

3. **최종 공격 토큰**  
   - 완성된 토큰의 형식은 아래와 같이 됩니다.
     ```
     Base64(Header_none) + "." + Base64(Payload_admin) + "."
     ```
   - 이 토큰을 쿠키에 삽입하면, 서버는 별도의 서명 검증 없이 관리자 권한으로 인식하여 `/admin-panel` 페이지를 오픈합니다.

## 공격 방법

1. **토큰 확인**  
   - 일반 사용자 계정(`testuser@test.com` / `password123`)으로 로그인합니다.
   - 로그인 후 쿠키에 저장된 JWT 토큰을 확인하거나, `/debug-token` 엔드포인트를 통해 Base64 디코딩된 Header와 Payload를 확인합니다.

2. **토큰 변조**  
   - **Header 수정**:  
     기존 Header (예시):
     ```json
     {
       "alg": "HS256",
       "typ": "JWT"
     }
     ```
     이를 아래와 같이 수정:
     ```json
     {
       "alg": "none",
       "typ": "JWT"
     }
     ```
   - **Payload 수정**:  
     기존 Payload (예시):
     ```json
     {
       "user_id": 1001,
       "role": "user",
       "exp": 1699999999
     }
     ```
     이를 아래와 같이 수정:
     ```json
     {
       "user_id": 1001,
       "role": "admin",
       "exp": 1699999999
     }
     ```
   - Header와 Payload를 각각 Base64 URL-safe 인코딩한 후, 서명 부분은 비워둔 채 `.`로 연결합니다.

3. **관리자 페이지 접근**  
   - 변조한 토큰을 브라우저의 쿠키에 삽입하거나, 개발자 도구를 통해 토큰 값을 변경합니다.
   - `/admin-panel` 페이지에 접근하면 관리자 권한으로 FLAG가 표시됩니다.

## 테스트 환경 실행

1. **Docker 이미지 빌드**
   ```bash
   docker build -t ctf-app .
2. **Docker 컨테이너 실행**
   ```bash
   docker run -d -p 5000:5000 ctf-app
3. **접속하기**
   웹 브라우저에서 http://localhost:5000 접속 후 로그인 (testuser@test.com / password123)


## 참고 사항

- 힌트:<br>
   ```/debug-token``` 엔드포인트 또는 프론트엔드 코드의 콘솔 로그 등을 확인하면, 토큰의 Base64 디코딩 결과를 얻을 수 있으므로, 변조에 대한 단서를 찾을 수 있습니다. 