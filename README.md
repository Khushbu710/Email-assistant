# AI Email Assistant

A Streamlit web app that generates professional or daily use emails using the latest open-source AI models via the Groq API.  
Simply enter your requirements and instantly get high-quality email drafts and improvement suggestions.

## Demo

Live app: https://email-assistant-710.streamlit.app/

## Features

- **AI-Powered Email Generation:** Quickly create emails for work, study, outreach, and more.
- **Improvement Suggestions:** Get actionable feedback to improve your drafts.
- **Fast & Free:** Powered by Groq’s Llama 3 models – no payment or credit card required.
- **Secure:** Your API key is stored as a secret on Streamlit Cloud, never in code.

## Getting Started

### Prerequisites

- Python 3.8+
- A free Groq API key ([Get one here](https://console.groq.com/keys))
- (Optional) [Streamlit Cloud](https://share.streamlit.io/) account for deployment

### Installation

1. **Clone this repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/your-repo-name.git
    cd your-repo-name
    ```

2. **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set your Groq API key:**

    - If running locally, create a file called `.env` in the root directory and add:
      ```
      GROQ_API_KEY="gsk_...your_api_key..."
      ```
    - If deploying on Streamlit Cloud, add your key in the app settings under "Secrets".

### Usage

Start the app locally:
```bash
streamlit run app.py
```

## Deployment (Streamlit Cloud)

1. Push your code to GitHub.
2. Go to [Streamlit Cloud](https://share.streamlit.io/) and create a new app.
3. Set your `GROQ_API_KEY` as a secret in the app’s settings.
4. Deploy & share your app link!

## File Structure

```
├── app.py                # Streamlit frontend
├── email_generator.py    # Groq-powered backend logic
├── requirements.txt      # Python dependencies
├── .env                  # Your API key (never commit this!)
├── .gitignore            # Ignore secrets and virtualenv
└── README.md             # This file
```

## Requirements

See `requirements.txt`:
```
streamlit
python-dotenv
groq
```

## Security

**Never commit your `.env` file or API keys to GitHub.**  
Use `.gitignore` to keep secrets safe.

## License

MIT

## Credits
Made by Khushbu Sharma

- [Groq API](https://groq.com/) – super-fast open-source model hosting.
- [Streamlit](https://streamlit.io/) – for easy web app deployment.
