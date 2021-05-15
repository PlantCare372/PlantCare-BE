# PlantCare BE
## How to run
- Để chạy backend chỉ cần gõ lệnh

```bash
    docker-compose up
```

## Note
- Lưu ý nếu máy có ứng dụng nào chạy ở port 80 thì nên tắt đi
- Nếu máy chạy Apache service ở port 80 có thể tắt 80
    ```bash
        sudo systemctl stop apache2.service (Linux)
    ```
- API sẽ được chạy ở localhost/api/v1
- Để xem API document mở localhost/redoc hoặc localhost/docs
- Để xem database vô localhost:5050 đăng nhập bằng
    - Username: admin@plantcare.com
    - Password: 123456789
    - Postgres server: db
    - Postgres username: postgres
    - Postgres password: 123456789
    - Database name: app

- Super user account
    - email: admin@plantcare.com
    - password: 123456789

## Progress
- [x] Hoàn tất API plant details
- [x] Hoàn tất API search plants
- [x] Hoàn tất API add, remove và list các favorite plant
- [x] Hoàn tất các API basic về user, bao gồm login, signup (create_user)
- [x] Hoàn tất API phân loại plants (trả về top 5 result với input là base64 string)