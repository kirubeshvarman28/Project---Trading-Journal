# 📊 Professional Trading Journal & Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A high-performance, locally-hosted trading journal designed for serious traders. Track your performance, analyze your psychology, and optimize your edge with advanced metrics and a proprietary **Zella Score**.

---

## ✨ Key Features

### 📈 Advanced Dashboard
- **Real-time Metrics**: Track Total PnL, Win Rate, Profit Factor, and Expectancy at a glance.
- **Visual Analytics**: Interactive cumulative and daily PnL charts powered by Chart.js.
- **Calendar View**: Monthly performance heatmap with weekly summaries.

### 🧠 Trading Psychology & Journaling
- **Daily Journal**: Log your mood, mistakes, and lessons learned to fight emotional trading.
- **Note Taking**: Dedicated notebook for market observations and strategy ideas.
- **Playbooks**: Document your setup rules with screenshots to ensure discipline.

### 🛡️ Risk & Account Management
- **Multi-Account Support**: Manage different accounts (funded, personal, demo) independently.
- **Lot Size Calculator**: Integrated tool to calculate position sizes based on risk %.
- **Metric Tracking**: Automated pip calculation for Forex and Gold (XAUUSD).

### 🎯 The Zella Score
Our proprietary algorithm evaluates your trading performance across 5 dimensions:
1. **Consistency**
2. **Profit Factor**
3. **Risk/Reward Ratio**
4. **Recovery Factor**
5. **Drawdown Management**

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite (via SQLAlchemy)
- **Frontend**: Bootstrap 5, Jinja2, Chart.js
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF

---

## 📂 Project Structure

```text
Project---Trading-Journal - Final/
├── app.py              # Application entry point & factory
├── models.py           # Database schemas (User, Trade, Account, etc.)
├── forms.py            # Web forms (Auth, Trade Input)
├── config.py           # App configuration
├── routes/             # Blueprint-based modular routing
│   ├── auth.py         # Login/Registration
│   ├── trades.py       # Trade logging & logic
│   ├── dashboard.py    # Main analytics engine
│   └── ...             # Other feature routes
├── templates/          # HTML templates (Jinja2)
├── static/             # CSS, JS, and uploaded screenshots
└── instance/           # Local SQLite database
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/kirubeshvarman28/Project---Trading-Journal.git
   cd Project---Trading-Journal
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install flask flask_sqlalchemy flask_login flask_wtf email_validator
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```
   Access the journal at `http://127.0.0.1:5000`

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*Developed with ❤️ by [Kirubeshvarman](https://github.com/kirubeshvarman28)*
