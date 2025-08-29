# BiteBerry

A modern recipe recommendation system that helps users discover personalized recipes based on their preferences, budget, and cooking time constraints. Features AI-powered recommendations and comprehensive meal planning tools.

## Features

### Core Functionality

- **Smart Recipe Recommendations**: AI-powered personalized suggestions using machine learning
- **Budget & Time Filtering**: Find recipes within your budget and available cooking time
- **Dietary Restrictions**: Support for vegetarian, vegan, gluten-free, and other dietary needs
- **User Preferences**: Customizable cooking preferences and constraints
- **Recipe Management**: Browse, search, and view detailed recipe information

### Advanced Features

- **Meal Planning**: Weekly meal planning with calendar view
- **Shopping Lists**: Auto-generate shopping lists from selected recipes
- **Recipe Likes**: Save and organize your favorite recipes
- **User Authentication**: Secure user registration and login system

## Tech Stack

### Backend

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Database for development
- **SentenceTransformers**: AI embeddings for recipe recommendations
- **Pytest**: Testing framework

### Frontend

- **React**: Modern JavaScript UI library
- **Vite**: Fast build tool and dev server
- **TailwindCSS**: Utility-first CSS framework
- **Axios**: HTTP client for API communication

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm

### Quick Setup (Recommended)

1. Clone the repository:

```bash
git clone https://git.cs.bham.ac.uk/projects-2024-25/axy483.git
cd BiteBerry
```

2. Make scripts executable and run setup:

```bash
chmod +x setup.sh start.sh
./setup.sh
```

3. Start both servers:

```bash
./start.sh
```

This will start both the backend (`http://localhost:8000`) and frontend (`http://localhost:5173`) servers.

### Manual Setup

<details>
<summary>Click to expand manual setup instructions</summary>

1. Clone the repository:

```bash
git clone https://git.cs.bham.ac.uk/projects-2024-25/axy483.git
cd BiteBerry
```

#### Backend Setup

2. Navigate to the backend directory:

```bash
cd backend
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Initialize the database:

```bash
python reset_db.py
```

5. Start the development server:

```bash
uvicorn main:app --reload
```

#### Frontend Setup

7. Navigate to the frontend directory:

```bash
cd frontend
```

8. Install dependencies:

```bash
npm install
```

9. Start the development server:

```bash
npm run dev
```

</details>

## API Documentation

Once the backend is running, you can access:

- **Interactive API docs**: `http://localhost:8000/docs`
- **Health check**: `http://localhost:8000/health`

### Key Endpoints

- `GET /api/recipes/` - Get all recipes
- `GET /api/recipes/recommend/{user_id}` - Get personalized recommendations
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/meal-planning/{user_id}` - Get meal plans
- `GET /api/shopping/{user_id}/lists` - Get shopping lists

## Testing

### Backend Tests

```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm run lint
```

## AI Recommendation System

BiteBerry features an advanced AI recommendation engine that uses:

- **SentenceTransformer embeddings** for recipe content analysis
- **Cosine similarity** for personalized matching
- **Hybrid filtering** combining user preferences and AI insights
- **Fallback mechanisms** for new users without preference history

## Configuration

### Environment Variables

- Backend configuration can be customized in `backend/core/config.py`
- Default preferences include £20 budget limit and 30-minute cooking time
- CORS is configured for frontend development servers

### Database

- Development uses SQLite (`biteberry.db`)
- Production-ready with SQLAlchemy ORM for easy database migration
- Includes proper indexing for performance optimization

## License

This project is part of an academic final project and is intended for educational purposes.

## Version

Current version: 2.0.0
