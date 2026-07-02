# ⚖️ AdalatMitra - AI Legal Assistant for Indian Courts

> Your AI-powered legal assistant that helps you search, track, and understand Indian court cases.

## 🎯 What is AdalatMitra?

AdalatMitra is a web application that helps users:
- 🔍 **Search Court Cases** by party name, case number, or CNR
- 📊 **Get Live Case Status** from Indian courts (High Court & District Court)
- 🤖 **Understand Legal Language** with AI-powered explanations
- 💬 **Ask Questions** about any case using AI chat
- 🌐 **Multi-Language Support** (English, Hindi, Tamil, Telugu, Marathi)

## 🏛️ Supported Courts

- ✅ **25+ High Courts** (Delhi, Bombay, Madras, Calcutta, etc.)
- ✅ **Supreme Court of India**
- ✅ **700+ District Courts** (All 36 states/UTs)

## 🚀 Key Features

| Feature | Description |
|---------|-------------|
| **Case Search** | Search by Party Name, Case Number, CNR, Advocate Name, FIR Number |
| **AI Summary** | Get simple language explanation of any case |
| **AI Chat** | Ask questions and get answers about your case |
| **Case Timeline** | View complete case history chronologically |
| **Multi-Language** | Generate summaries in 10+ Indian languages |
| **Auto-CAPTCHA** | No manual CAPTCHA entry required - automatic solving |
| **Court Selection** | Switch between High Court and District Court |
| **Advanced Filters** | Filter by status, case type, CNR, party name |

## 🛠️ Technology Stack

### Backend
- **Python 3.11+** - Core language
- **Streamlit** - Web framework
- **Bharat Courts SDK** - Court data integration
- **Gemini + Groq** - AI/LLM with automatic fallback

### Frontend
- **Streamlit Components** - Interactive UI
- **Custom CSS** - Modern, clean design

### AI & ML
- **EasyOCR** - Automatic CAPTCHA solving
- **LangChain** - AI orchestration
- **Sentence Transformers** - Text embeddings
- **Qdrant** - Vector database (for RAG)

## 📁 Project Structure
AdalatMitra/
├── frontend/ # Streamlit UI
│ ├── components/ # UI components
│ ├── pages/ # Multi-page navigation
│ └── styles/ # Custom CSS
├── agents/ # Business logic
│ ├── case_agent.py # Case search & retrieval
│ ├── explanation_agent.py # AI explanations
│ ├── timeline_agent.py # Case timeline builder
│ └── query_router.py # Intent detection
├── services/ # External integrations
│ ├── bharat_court_service.py
│ ├── ai_gateway.py
│ └── captcha_solver.py
├── state/ # Session management
├── config/ # Configuration
└── utils/ # Helpers & constants

## 🔧 Installation

### Prerequisites
- Python 3.11 or higher
- Docker (optional, for local Qdrant)

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/AdalatMitra.git
cd AdalatMitra

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# 5. Run the application
python run.py

# Required
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
HF_TOKEN=your_huggingface_token

# Optional
DEFAULT_COURT=delhi
DEFAULT_YEAR=2024
LOG_LEVEL=INFO

🎯 Usage Guide
1. Search for Cases
By Party Name:

text
Party Name: Union of India
Year: 2024
Status: Pending
By Case Number:

text
Case Number: 355/2024
Year: 2024
2. Understand a Case
Click Details on any case

View the AI-generated summary

Ask questions in the AI Chat

3. District Court Search
Select District Court radio button

Choose State and District

Enter party name and search
# flow digram
User → Streamlit UI → Query Router → Case Agent → Bharat Courts API
                                          ↓
                                    AI Gateway (Gemini/Groq)
                                          ↓
                                    Explanation Agent
                                          ↓
                                    Translation Agent
                                          ↓
                                    User Response
