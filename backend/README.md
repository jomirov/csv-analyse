## Цель проекта
Создание локального API, который принимает текст учебной поставки в CSV, проверяет структуру и строки и возвращает отчёт об ошибках.
1. Создание POST /preview, с единственным запрашиваемым полем csv_text.
2. Проверка текста: заголовок таблицы, количество строк и значения полей.
3. Создание отчёта об ошибках на основе проверки текста.
4. Автоматизированное тестирование.

## Тест
| Что проверить | Ожидаемый результат |
|---------------|---------------------|
| Правильный CSV | Три строки с количеством 1, 2, 3 дают total=3, valid=3, invalid=0. |
| Ошибка одной строки | Количество 0 дает 200 с ошибкой строки, две остальные строки остаются пригодными |
| Повтор кода | Второя появление A01 помечено duplicate_code; число строк не меняется |
| Границы входа | Неверный заголовк дает 400; текст больше 100000 байт дает 413; путь ../A остается обычным неверным значением |

## Запуск (PowerShell)
Подготовка окружения:
```powershell
cd backend
py -m venv .venv
.venv/Scripts/activate
python -m pip install -r requirements.txt
```
Запуск локального сервера:
```powershell
uv run fastapi dev
```
### POST-запросы по /preview
Запрос с правильным CSV:
```powershell
curl http://localhost:8000/preview `
-Method POST `
-Headers @{"Content-Type"="application/json"} `
-Body '{"csv_text": "item_code,quantity,location;A01,2,R1;B02,5,R2"}'
```
Ожидаемый ответ:
```json

```
Запрос с ошибкой строки (quantity):
```powershell
curl http://localhost:8000/preview `
-Method POST `
-Headers @{"Content-Type"="application/json"} `
-Body '{"csv_text": "item_code,quantity,location;A01,0,R1;B02,5,R2"}'
```
Запрос с дубликатом кода (item_code):
```powershell
curl http://localhost:8000/preview `
-Method POST `
-Headers @{"Content-Type"="application/json"} `
-Body '{"csv_text": "item_code,quantity,location;A01,1,R1;A01,5,R2"}'
```
Запрос с неправильным заголовком:
```powershell
curl http://localhost:8000/preview `
-Method POST `
-Headers @{"Content-Type"="application/json"} `
-Body '{"csv_text": "item_odec,quantity,location;A01,1,R1;A01,5,R2"}'
```
### Запуск тестов
```powershell
uv run pytest
```