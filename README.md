#  ProjectManager

Aplikacja do zarządzania projektami z autoryzacją JWT, architekturą SOLID i kompletnymi testami.

##  Stack

**Backend:** Flask 3.0 + SQLAlchemy 2.0 | **Frontend:** Vue.js 3 + Pinia + Tailwind CSS

##  Quick Start

### Backend
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py  # http://127.0.0.1:5000
```

### Frontend
```bash
cd frontend
npm install
npm run dev  # http://localhost:3001
```

### Uruchamianie testów
```bash
cd backend
.\venv\Scripts\Activate.ps1
pytest tests/ -v
```

##  Funkcje

-  Rejestracja/logowanie (JWT)
-  Zarządzanie projektami (Owner/Member)
-  Zadania (To do  In progress  Done)
-  Dark/Light mode
-  Współpraca w zespołach

##  Architektura (SOLID)

```
Routes (HTTP)  Services (Logika biznesowa)  Models (Baza danych)
```

##  Technologie

| Backend | Frontend | Testing |
|---------|----------|---------|
| Flask 3.0.0 | Vue.js 3 | pytest 8.0.0 |
| SQLAlchemy 2.0.36 | Pinia | pytest-flask 1.3.0 |
| Flask-JWT-Extended 4.6.0 | Tailwind CSS | pytest-cov 4.1.0 |
| SQLite | Axios | 6 testów (3 unit + 3 integration) |
| Python 3.13+ | Vite | 100% pass rate |

##  Testowanie

### Unit Tests (3)
- `test_user_password.py` - hashowanie haseł
- `test_project_creation.py` - tworzenie projektów
- `test_task_creation.py` - tworzenie zadań

### Integration Tests (3)
- `test_auth_flow.py` - rejestracja → logowanie → autoryzacja
- `test_projects_endpoints.py` - CRUD projektów przez API
- `test_tasks_endpoints.py` - lista zadań projektu

### Uruchomienie testów
```bash
cd backend
.\venv\Scripts\Activate.ps1
pytest tests/ -v                    # wszystkie testy
pytest tests/unit/ -v               # tylko unit
pytest tests/integration/ -v        # tylko integration
pytest tests/ --cov=app            # z coverage
```

##  Wymagania

- **Python**: 3.13 lub nowszy
- **Node.js**: 18 lub nowszy
- **npm**: 9 lub nowszy