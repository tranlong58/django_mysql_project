# django_mysql_project

- 'api': các api CRUD các transaction của app wallet. 
- 'home': code phần home page.
- 'mysite': thư mục gốc của project.
- 'nginx': file cấu hình nginx.
- 'wallet': code phần wallet page.
- 'tts':
    - 'views': api_view để gọi api và LoginView cho chức năng login (generate token).
    - 'services': adapter cho việc dùng api 3rd (FakeYou) và service gọi api 3rd.
    - 'middleware': middleware cho việc xác thực token của request.
    - 'exceptions': custom exceptions xử lý khi xác thực token thất bại.
