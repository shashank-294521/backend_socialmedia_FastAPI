# backend_socialmedia_FastAPI

# Social Media Backend (FastAPI + PostgreSQL)

A backend API for a **social media platform**, built with **FastAPI** and **PostgreSQL**.  
Implements core features like authentication, user management, posts, messaging, following, profiles, and voting.

---

## 🚀 Features

- **Authentication & Authorization**
  - User registration & login with JWT
  - Secure password hashing
  - Token-based authentication

- **Users & Profiles**
  - Manage user profiles
  - Follow / Unfollow users
  - Get followers & following list

- **Posts**
  - Full CRUD (create, read, update, delete)
  - Ownership-based permissions
  - Voting system (likes/dislikes)

- **Messaging**
  - Direct user-to-user messages
  - Conversation tracking

- **Votes**
  - Upvote / Downvote posts
  - Track popularity of posts

---

## 🛠 Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)  
- **Database:** PostgreSQL  
- **ORM:** SQLAlchemy  
- **Auth:** OAuth2 + JWT  
- **Validation:** Pydantic schemas  
- **Config & Utils:** Custom utility functions + `.env`  

---

## 📂 Project Structure

backend_socialmedia_FastAPI/
│── app/
│ ├── init.py
│ ├── config.py # App configuration
│ ├── database.py # PostgreSQL connection
│ ├── main.py # Application entry point
│ ├── oauth2.py # JWT & authentication utilities
│ ├── schemas.py # Pydantic models
│ ├── utils.py # Helper functions
│ │
│ └── routers/ # API routers
│ ├── auth.py
│ ├── follow.py
│ ├── message.py
│ ├── post.py
│ ├── profile.py
│ ├── user.py
│ └── votes.py
│
│── .env # Environment variables
│── requirements.txt # Project dependencies

yaml
Copy code

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/shashank-294521/backend_socialmedia_FastAPI.git
cd backend_socialmedia_FastAPI
2. Create & activate a virtual environment
bash
Copy code
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
4. Setup PostgreSQL
Create a database (e.g. socialmedia_db)

Update your .env file:

ini
Copy code
DATABASE_URL=postgresql://username:password@localhost:5432/socialmedia_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
5. Run the server
bash
Copy code
uvicorn app.main:app --reload
📖 API Documentation
After running the server:

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc

🔮 Future Improvements
Real-time chat with WebSockets

Notifications system

File uploads for profile pictures & posts

Recommendations & trending feed

📜 License
MIT License.

yaml
Copy code

---

This one now **starts with `uvicorn app.main:app --reload`** and **matches your `app/` + `routers/` structure**.  

👉 Do you want me to also add a **sample `.env` file template** inside the README so contributors can copy-paste it directly?
