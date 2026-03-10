# CINEWHY

**CineWhy** is a next-generation, premium cinematic discovery and recommendation engine. Powered by intelligent semantic data inferences and an ultra-chic 3D neon user interface, CineWhy pushes the boundaries of how users find and explore movies.

## 🌟 Features

- **Semantic Discovery Engine**: Go beyond basic genre filtering. CineWhy scores over 2,000+ movies using a custom semantic accuracy algorithm, returning exact matches based on complex variables like release decades, runtime preferences, and cinematic tones.
- **Premium 3D UI UX**:
  - **Dynamic Glassmorphism**: High-fidelity frosted glass components over deeply blurred cinematic backgrounds.
  - **Fluid Reactive Cards**: Every movie card transforms in responsive 3D space, tracking your cursor movements to create an immersive, tactile experience.
  - **Cinematic Gradients**: Algorithmic color-grading dynamically generates deep Violet, Crimson, and Emerald neon glows based on movie metadata.
- **Flawless 4K Poster Integration**: Auto-resolves over 220+ hardcoded poster endpoints against TMDB's high-resolution `/original/` API to guarantee sharp, stunning visual quality across every display.
- **Command Center Architecture**: A unified sidebar navigation system offering instant, zero-reload transitions between the Welcome Dashboard, Filter Engine, Discovery Results, and Analytics tracking.

## 🚀 Tech Stack

### Frontend Architecture
- **React 18** & **Vite**: Ultra-fast component rendering and hot module replacement.
- **Tailwind CSS v3**: For utility-first styling, complex CSS gradients, and responsive layouts.
- **Framer Motion**: Orchestrates complex layout transitions, 3D rotations, and staggering entry animations.
- **Lucide React**: Clean, consistent vector iconography.
- **React Router**: Client-side routing for the dashboard architecture.

### Backend Infrastructure
- **Python 3.10+**: Core backend scripting language.
- **Flask**: Lightweight WSGI web application framework serving RESTful JSON APIs.
- **Flask-CORS**: Handles robust cross-origin resource sharing between the Vite dev server and Python backend.
- **Custom Inference Engine**: Normalizes metadata (1/10 rating scales, deduplication), applies hard-constraints, and calculates percentage-based match accuracies.

## 🛠️ Installation & Setup

### Prerequisites
- Node.js (v18+ recommended)
- Python (v3.10+ recommended)

### 1. Clone the Repository
```bash
git clone https://github.com/mounibwassim/CINEWHY.git
cd CINEWHY
```

### 2. Backend Setup (Flask Server)
Navigate to the root directory and install Python dependencies.
```bash
pip install flask flask-cors
```
Start the backend discovery server:
```bash
python webapp.py
```
*The server will run locally on `http://localhost:5000`.*

### 3. Frontend Setup (React/Vite)
Open a new terminal window, navigate to the `frontend` directory, and install Node dependencies.
```bash
cd frontend
npm install
```
Start the frontend development server:
```bash
npm run dev
```
*The application UI will render at `http://localhost:5173`.*

## 🎥 Usage Guide

1. **Dashboard Home**: Start at the Welcome screen, outlining system health, total datasets loaded, and active inference algorithms.
2. **Filter Engine**: Configure your search. Select positive genres (Action, Sci-Fi), negative genres (exclude Rom-Coms), adjust the temporal timeline (e.g., 1990-2024), and dictate runtime constraints.
3. **Discovery Results**: Engage with the Discovery Grid. Every card features a dynamic 4K TMDB poster, a deterministic neon gradient, and interactive 3D hover states. Click a movie to view deep analytics and the exact logic algorithm behind why it was recommended for you. 

## ⚖️ License
Proprietary software. All rights reserved by the original authors and maintainers. Not licensed for open-source modification without explicit permission.

---
*Built with ❤️ for cinephiles everywhere. Enjoy the magic of cinema.*
