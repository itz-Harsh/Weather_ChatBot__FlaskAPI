# 🌤️ Weather ChatBot

A tiny, stylish frontend + Flask backend that returns current weather for a city using OpenWeatherMap. Built for local development and quick testing.

---

## 🚀 What it does

Enter a city name in the input box on the page. When the field changes, the frontend calls the Flask API at `http://127.0.0.1:5000/weather` and shows a small weather summary (temperature, description, humidity, wind).

## 🧭 Repo layout

- `app.py` — Flask backend (exposes `/weather`).
- `index.html`, `script.js`, `style.css` — frontend static files.
- `.env` — store your OpenWeatherMap API key here (not committed).

## ✅ Requirements

- Python 3.8+ (Windows)
- An OpenWeatherMap API key (get one at https://openweathermap.org/)

## 🛠️ Setup (PowerShell)

Open PowerShell in the project folder and run:

```powershell
# create virtual env
python -m venv .venv

# activate
.\.venv\Scripts\Activate.ps1

# install dependencies
pip install flask requests python-dotenv flask-cors
```

Create or update `.env` in the project root with your API key:

```properties
apikey=YOUR_OPENWEATHERMAP_KEY
```

Note: The repo already includes a `.env` placeholder — keep it private.

## ▶️ Run the backend

With the venv active:

```powershell
python app.py
```

This starts the Flask API at `http://127.0.0.1:5000` (the same base URL used in `script.js`).

## 🌐 Open the frontend

You can open `index.html` directly in the browser, but using a local HTTP server is more reliable (avoids file:// restrictions):

```powershell
# serve current folder at http://127.0.0.1:8000
python -m http.server 8000
```

Then open `http://127.0.0.1:8000/index.html` in your browser.

## 🧪 How to use

- Type a city name into the input. When the input loses focus (change event), the page will call the API and display results.

Tip: If you want immediate results while typing, change `onchange` to `oninput` in `index.html` or add a keypress listener in `script.js`.

## 🔍 Troubleshooting

- If nothing happens, open DevTools (F12) → Console/Network and check for errors.
- CORS errors: ensure the backend is running. `app.py` already enables CORS.
- Connection errors: confirm Flask started on port `5000` and `.env` has a valid key.

## ❤️ Credits

Made with Flask + OpenWeatherMap. Style by `style.css`.

---
