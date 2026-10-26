# Python REST API & Database Service
Django REST Framework API for company resources with five related models, CRUD, validation, search, filtering, ordering, pagination, authentication, structured errors, automated tests, and a Postman collection.

## Five linked tables
- Department: has employees and projects.
- Employee: belongs to a department; can have assets and project assignments.
- Project: belongs to a department.
- Assignment: links an employee and project.
- Asset: optionally assigned to an employee.

## Run on Windows PowerShell
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
API base URL: `http://127.0.0.1:8000/api/`

## MySQL (optional)
Create a MySQL database and user, then set environment variables:
```sql
CREATE DATABASE company_api CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'company_api_user'@'localhost' IDENTIFIED BY 'choose-a-strong-password';
GRANT ALL PRIVILEGES ON company_api.* TO 'company_api_user'@'localhost';
FLUSH PRIVILEGES;
```
```powershell
$env:DB_ENGINE="mysql"
$env:DB_NAME="company_api"
$env:DB_USER="company_api_user"
$env:DB_PASSWORD="your-password"
$env:DB_HOST="127.0.0.1"
$env:DB_PORT="3306"
python manage.py migrate
python manage.py runserver
```
SQLite is the default. MySQL mode requires MySQL Server and `mysqlclient`. Never commit real credentials.

## API routes
`/departments/` and `/departments/{id}/`
`/employees/` and `/employees/{id}/`
`/projects/` and `/projects/{id}/`
`/assignments/` and `/assignments/{id}/`
`/assets/` and `/assets/{id}/`
`/health/` and `/dashboard/`

These are 12 primary URL patterns; CRUD uses GET, POST, PUT, PATCH and DELETE where applicable. This is not a claim of 12 individual HTTP method combinations.

Search/filter examples: `/api/employees/?search=Ananya`, `/api/employees/?department=1`, `/api/employees/?ordering=-salary`, `/api/assets/?status=available`.

Anonymous users can read; write operations require authentication. Run `python manage.py test`. Import `postman/collection.json` into Postman. Use your own local credentials and real IDs.
