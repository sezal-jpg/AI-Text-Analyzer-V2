TextShield AI — Privacy-Aware Intelligent Text Analysis

TextShield AI is a privacy-focused text analysis application that combines a multi-layer PII firewall, Azure AI Language services, and the Qwen 2.5 1.5B instruction-tuned language model to analyze and continue user-provided text.

The application is designed around a simple principle:
Detect and remove sensitive information before sending text to downstream AI and language-analysis services.

🚀 Live Demo

Azure Deployment:
https://sezal-jpg.github.io/AI-Text-Analyzer-V2/
GitHub Repository:
https://github.com/sezal-jpg/AI-Text-Analyzer-V2

✨ Features
- 🔐 PII detection and redaction
- 🛡️ Multi-layer privacy firewall
- 😊 Sentiment analysis
- 🔑 Key phrase extraction
- 👤 Named entity recognition
- ✍️ AI text continuation using Qwen
- 📊 Text statistics
- 🐳 Dockerized deployment
- ☁️ Azure Container Apps deployment
- 📦 Azure Container Registry for container images

🏗️ Architecture
                         User Input
                             │
                             ▼
                    ┌─────────────────┐
                    │   PII Firewall  │
                    └────────┬────────┘
                             │
                  Detect + Validate + Redact
                             │
                             ▼
                     Sanitized Text
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
       ┌──────────────────┐      ┌────────────────────┐
       │ Azure AI Language│      │ Qwen 2.5 1.5B      │
       │                  │      │ Instruct Model     │
       │ • Sentiment      │      │                    │
       │ • Key Phrases    │      │ • Text Generation  │
       │ • Entities       │      │                    │
       └────────┬─────────┘      └─────────┬──────────┘
                │                          │
                └────────────┬─────────────┘
                             ▼
                         Dashboard
The key privacy principle is that the original text passes through the PII firewall first. Downstream analysis and generation operate on the privacy-sanitized text.

🔐 Privacy Firewall
The PII firewall is the core security layer of TextShield AI.
It uses multiple detection layers:
1. Azure AI Language PII detection
2. Category-specific confidence thresholds
3. Context-aware rules
4. Deterministic validation rules
5. Secret/API-key detection
6. Overlap handling and deduplication
7. Right-to-left redaction
Sensitive information is redacted before the sanitized text is passed to the downstream analysis and generation components.

PII Categories
The firewall currently handles categories and patterns such as:
- Email addresses
- Phone numbers
- Indian PAN numbers
- Aadhaar-related information
- Bank account information
- Credit card numbers
- Dates of birth
- API keys and secrets
- Password/token patterns
The application also applies validation and contextual rules to reduce false positives.

PII Firewall Pipeline
Raw Text
   │
   ▼
Azure PII Detection
   │
   ▼
Confidence Thresholds
   │
   ▼
Context Rules
   │
   ▼
Deterministic Validators
   │
   ▼
Secret Detection
   │
   ▼
Merge / Deduplicate
   │
   ▼
Right-to-Left Redaction
   │
   ▼
Sanitized Text
   │
   ├──────────────► Azure AI Language
   │
   └──────────────► Qwen Generation
Only the sanitized text is sent to the downstream language-analysis and generation components.

🧠 AI Capabilities

Sentiment Analysis
Azure AI Language analyzes the privacy-sanitized text and returns:
- Positive sentiment
- Neutral sentiment
- Negative sentiment
- Confidence scores

Key Phrase Extraction
The application extracts important concepts and phrases from the sanitized text.

Named Entity Recognition
Azure AI Language identifies entities present in the sanitized text.

AI Text Continuation
TextShield AI uses:
Qwen/Qwen2.5-1.5B-Instruct

The model generates a continuation based on the privacy-sanitized text rather than the original raw input.

The generation service also applies instructions to:
- Avoid repeating the original text
- Stay on the same topic
- Avoid generating sensitive information that was not present in the sanitized text
- Avoid unrelated information
- Produce complete sentences

Text Statistics
The dashboard provides:
- Word count
- Character count
- Sentence count
- Estimated reading time

🛠️ Technology Stack
Frontend
- Streamlit
AI / Machine Learning
- Hugging Face Transformers
- Qwen/Qwen2.5-1.5B-Instruct
- PyTorch

Azure
- Azure AI Language
- Azure Container Registry
- Azure Container Apps

Deployment
- Docker
- Azure Container Registry
- Azure Container Apps

Programming Language
- Python

📁 Project Structure
AI-Text-Analyzer-V2/
│
├── services/
│   ├── __init__.py
│   ├── generation_service.py
│   ├── language_service.py
│   └── pii_service.py
│
├── utils/
│   ├── __init__.py
│   └── text_stats.py
│
├── .dockerignore
├── .gitignore
├── app.py
├── containerapp.yaml
├── Dockerfile
├── probe-config.yaml
├── README.md
└── requirements.txt

💻 Local Setup

1. Clone the repository
git clone https://github.com/sezal-jpg/AI-Text-Analyzer-V2.git
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

🐳 Docker
Build the Docker image
docker build -t textshield-ai .
Run the container
docker run -p 8501:8501 --env-file .env textshield-ai
Open:
http://localhost:8501

☁️ Azure Deployment
The application is containerized and deployed using:
Docker
   │
   ▼
Azure Container Registry
   │
   ▼
Azure Container Apps
Azure Container Registry
Azure Container Registry stores the Docker image used by the application.
Azure Container Apps
Azure Container Apps runs the application as a containerized cloud service with external HTTPS access.
Secrets
Azure secrets are configured separately from the Docker image so that Azure credentials are not stored inside the application source code or container image.

Deployment Configuration
The deployed application uses:
- Azure Container Apps
- Azure Container Registry
- User-assigned managed identity for registry access
- Azure AI Language credentials stored as an Azure secret
- 2 CPU
- 4 GiB memory
- Streamlit on port 8501

🔒 Security Design
TextShield AI follows a privacy-first processing flow:
User Input
    │
    ▼
PII Firewall
    │
    ▼
Sensitive Information Redacted
    │
    ▼
Sanitized Text
    │
    ├──────────────► Azure AI Language
    │
    └──────────────► Qwen Model
This ensures that downstream analysis and generation components receive the sanitized version of the text.
The PII firewall combines Azure's PII detection capabilities with application-level thresholds, contextual rules, deterministic validation, secret detection, and redaction logic.

⚠️ Important Security Note
TextShield AI is an educational and portfolio project demonstrating privacy-aware AI application design.
It should not be considered a complete enterprise Data Loss Prevention (DLP) solution or a guarantee of zero data leakage.
Production systems should include additional controls such as:
- Secure networking
- Centralized secret management
- Access management
- Controlled logging
- Monitoring and alerting
- Security testing
- Stronger enterprise-grade DLP controls
- Additional content-safety controls where required
Content safety and inappropriate-content detection are considered future improvements and are outside the primary scope of the current project.

🎯 Project Goals
The project demonstrates how a privacy layer can be placed in front of AI-powered text-processing systems.
The main design goal is:
Privacy First → Analyze Safely → Generate Responsibly

The project focuses primarily on:
- Protecting sensitive information
- Performing useful text analysis
- Applying AI generation to sanitized text
- Demonstrating practical privacy-aware AI architecture
- Deploying the complete application as a cloud-hosted containerized service

🚀 Future Improvements
Possible future enhancements include:
- Advanced content-safety and inappropriate-content detection
- Stronger output moderation
- Larger and more capable language models
- Additional PII categories
- Enterprise-grade DLP integration
- Authentication and user management
- Audit logging
- Advanced monitoring and observability
- Secure private networking
- More extensive security testing

👩‍💻 Author
Sezal
BTech — Artificial Intelligence & Machine Learning

📌 Project Links
Live Application:
https://sezal-jpg.github.io/AI-Text-Analyzer-V2/
GitHub:
https://github.com/sezal-jpg/AI-Text-Analyzer-V2