# TextShield AI — Privacy-Aware Intelligent Text Analysis

TextShield AI is a privacy-focused text analysis application that combines PII protection, Azure AI Language services, and a local Qwen language model to analyze and continue user-provided text.

The application is designed around a simple principle:

> Detect and remove sensitive information before sending text to downstream
> AI and language-analysis services.


## Features

- 🔐 PII detection and redaction
- 🛡️ Multi-layer privacy firewall
- 😊 Sentiment analysis
- 🔑 Key phrase extraction
- 👤 Named entity recognition
- ✍️ AI text continuation using Qwen
- 📊 Text statistics
- ☁️ Dockerized deployment
- ☁️ Azure Container Apps deployment


## Architecture

```text
                 User Input
                     │
                     ▼
              ┌──────────────┐
              │ PII Firewall │
              └──────┬───────┘
                     │
          Detect + Validate + Redact
                     │
                     ▼
              Sanitized Text
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
 ┌──────────────────┐   ┌──────────────────┐
 │ Azure AI Language│   │ Qwen 2.5 1.5B   │
 │                  │   │ Instruct Model   │
 │ • Sentiment      │   │                  │
 │ • Key Phrases    │   │ Text Generation  │
 │ • Entities       │   └──────────────────┘
 └────────┬─────────┘
          │
          ▼
       Dashboard

Privacy Firewall

The PII firewall is the core security layer of TextShield AI.
It uses multiple detection layers:
1. Azure AI Language PII detection
2. Category-specific confidence thresholds
3. Context-aware rules
4. Deterministic validation rules
5. Secret/API-key detection
6. Overlap handling and deduplication
7. Right-to-left redaction
Sensitive information is redacted before the sanitized text is passed to
the downstream analysis and generation components.
The firewall currently handles categories such as:
- Email addresses
- Phone numbers
- Indian PAN numbers
- Aadhaar-related information
- Bank account information
- Credit card numbers
- Dates of birth
- API keys and secrets
- Password/token patterns
The application also applies validation and contextual rules to reduce
false positives. 

Technology Stack
Frontend
- Streamlit
AI / Machine Learning
- Hugging Face Transformers
- Qwen/Qwen2.5-1.5B-Instruct
- PyTorch
Azure
- Azure AI Language
- Azure Container Apps
- Azure Container Registry
Deployment
- Docker
- Azure Container Apps
Programming Language
- Python

Project Structure
 AI-Text-Analyzer-V2/
│
├── app.py
│
├── services/
│   ├── __init__.py
│   ├── pii_service.py
│   ├── language_service.py
│   └── generation_service.py
│
├── utils/
│   ├── __init__.py
│   └── text_stats.py
│
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .env.example
├── .gitignore
└── README.md

Local Setup

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd AI-Text-Analyzer-V2

2. Create a virtual environment
python -m venv venv

Activate it on Windows:
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Configure environment variables
Create a .env file:
AZURE_LANGUAGE_ENDPOINT=your_azure_language_endpoint
AZURE_LANGUAGE_KEY=your_azure_language_key

Never commit the .env file or Azure credentials to GitHub.
5. Run the application
streamlit run app.py

The application will be available at:
http://localhost:8501

Docker
Build the Docker image:
docker build -t textshield-ai .

Run the container:
docker run -p 8501:8501 --env-file .env textshield-ai

Open:
http://localhost:8501

Azure Deployment
The application is containerized and deployed using:
Docker
   ↓
Azure Container Registry
   ↓
Azure Container Apps

Azure Container Registry stores the Docker image, while Azure Container Apps
runs the application as a containerized service.
Azure secrets are configured separately from the Docker image so that
credentials are not stored inside the application source code.
How the PII Firewall Works
Raw Text
   ↓
Azure PII Detection
   ↓
Confidence Thresholds
   ↓
Context Rules
   ↓
Deterministic Validators
   ↓
Secret Detection
   ↓
Merge / Deduplicate
   ↓
Redaction
   ↓
Sanitized Text

Only the sanitized text is sent to the downstream language-analysis and
generation components.
The application then performs analysis on the sanitized version.

Important Security Note

TextShield AI is an educational and portfolio project demonstrating
privacy-aware AI application design.
It should not be considered a complete enterprise Data Loss Prevention
(DLP) solution or a guarantee of zero data leakage.
Production systems should include additional controls such as secure
networking, centralized secret management, logging controls, access
management, monitoring, and security testing.

Project Goals

The project demonstrates how a privacy layer can be placed in front of
AI-powered text-processing systems.

The main design goal is:
Privacy First → Analyze Safely → Generate Responsibly

Author

Sezal
BTech — Artificial Intelligence & Machine Learning
