# BNPL (Buy Now Pay Later) Application

This project implements a Buy Now Pay Later (BNPL) system with a Django REST Framework backend and React frontend.

---

## Features

- Merchants create BNPL plans with equal installments.
- Users view their plans and installments in a calendar or dashboard.
- Role-based login and views for merchants and users.
- User can pay installments one by one.
- Automatic plan status updates when all installments are paid.

---

## Tech Stack

- Backend: Django, Django REST Framework
- Frontend: React, Axios
- Authentication: Token-based (DRF TokenAuth)

---

## Prerequisites

- Python 3.8+
- Node.js 14+ and npm or yarn
- PostgreSQL or SQLite (default Django DB)
- Git

---

## Backend Setup (Django)

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd MainProject
Create and activate a virtual environment:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
Install Python dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Configure environment variables:

Create a .env file (or set environment variables) with:

env
Copy
Edit
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3   # Or your PostgreSQL URL
Run migrations:

bash
Copy
Edit
python manage.py migrate
Create a superuser (optional):

bash
Copy
Edit
python manage.py createsuperuser
Run the backend server:

bash
Copy
Edit
python manage.py runserver
Frontend Setup (React)
Navigate to frontend folder:

bash
Copy
Edit
cd bnpl-frontend
Install dependencies:

bash
Copy
Edit
npm install
# or
yarn install
Configure environment variables:

Create a .env file in bnpl-frontend with:

env
Copy
Edit
REACT_APP_API_BASE_URL=http://localhost:8000
Run the React development server:

bash
Copy
Edit
npm start
# or
yarn start
The app will be available at http://localhost:3000

Notes
Make sure the backend server (localhost:8000) is running before starting the frontend.

Use the API token generated at login for authenticated requests (stored in localStorage).

Tailwind CSS is used for styling; if you encounter issues, ensure Tailwind is properly installed and built.

For role-based redirects and calendar views, see the frontend components.
