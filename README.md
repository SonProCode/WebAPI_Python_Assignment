# Web API SensorData bằng Python FastAPI

Dự án này là bản triển khai Python tương đương tutorial Web API trong file đề bài. API dùng FastAPI để tạo Swagger tự động và dùng MongoDB để lưu dữ liệu cảm biến.

## 1. Cài môi trường

```powershell
cd D:\WebAPI_Python_Assignment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Chạy MongoDB

Nếu dùng Docker:

```powershell
docker run -d -p 27017:27017 --name mongodb mongo
```

Nếu máy đã cài MongoDB, chỉ cần bảo đảm dịch vụ đang chạy tại:

```text
mongodb://localhost:27017
```

## 3. Cấu hình

Sao chép `.env.example` thành `.env` nếu muốn chỉnh cấu hình:

```powershell
copy .env.example .env
```

## 4. Chạy API

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 5000
```

Mở Swagger:

```text
http://127.0.0.1:5000/docs
```

## 5. API có trong project

| Method | API | Chức năng |
|---|---|---|
| GET | `/api/AppVersion` | Lấy version app |
| POST | `/api/PostVersion` | Gửi version từ thiết bị |
| GET | `/api/SensorDatas` | Lấy danh sách dữ liệu cảm biến |
| GET | `/api/SensorDatas/{id}` | Lấy dữ liệu theo ID |
| POST | `/api/SensorDatas` | Thêm dữ liệu cảm biến |
| PUT | `/api/SensorDatas/{id}` | Cập nhật dữ liệu |
| DELETE | `/api/SensorDatas/{id}` | Xóa dữ liệu |

## 6. Body mẫu

POST `/api/SensorDatas`

```json
{
  "deviceId": "DEVICE_001",
  "temperature": 30.5,
  "humidity": 70.2,
  "createdAt": "2026-05-09T10:00:00"
}
```

POST `/api/PostVersion`

```json
{
  "deviceId": "DEVICE_001",
  "version": 1
}
```

## 7. Test bằng curl

```powershell
curl -X POST http://127.0.0.1:5000/api/SensorDatas `
  -H "Content-Type: application/json" `
  -d "{\"deviceId\":\"DEVICE_001\",\"temperature\":30.5,\"humidity\":70.2}"
```

```powershell
curl http://127.0.0.1:5000/api/SensorDatas
curl http://127.0.0.1:5000/api/AppVersion
```
