# 🚀 Moves

Moves is a full-stack web application that recommends nearby places based on a user's current mood. Users can discover restaurants, coffee shops, gyms, shopping centers, and other locations using the Google Places API, then save their favorite places for future visits.

---

## Features

- User authentication (Sign Up / Login / Logout)
- Persistent user sessions
- Mood-based recommendations
- Google Places integration
- Save and manage bookmarks
- Responsive React frontend
- MySQL database persistence

---

## Tech Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- Flask
- Flask-CORS

### Database

- MySQL

### APIs

- Google Places API

### Development Tools

- Git
- GitHub
- Postman
- MySQL Workbench

---

## Project Structure

```
moves/
│
├── backend/
│   ├── database/
│   ├── routes/
│   ├── services/
│   └── app.py
│
├── src/
│   ├── Components/
│   └── assets/
│
├── package.json
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Moves.git
cd Moves
```

Install frontend dependencies

```bash
npm install
```

Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

---

## Configuration

Create a `.env` file and add your Google Places API key.

```
GOOGLE_API_KEY=YOUR_API_KEY
```

Configure your MySQL credentials in:

```
backend/database/connection.py
```

---

## Running the Application

Start the frontend and backend:

```bash
npm run dev
```

Frontend

```
http://localhost:5173
```

Backend

```
http://127.0.0.1:5555
```

---

## Future Improvements

- AI-powered recommendation explanations
- User profiles
- Recommendation history
- Personalized recommendations
- Map integration
- Cloud deployment

---

## Author

Jesus Lopez

Bachelor of Science in Computer Science
