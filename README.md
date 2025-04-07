# PitchSlap - AI Startup Idea Generator

PitchSlap is an AI-powered application that generates unique startup ideas based on user requirements. It uses OpenAI's GPT-4o model to create innovative, market-ready business concepts.

## Architecture

- **Backend**: FastAPI application deployed on Google Cloud Run
- **Frontend**: Streamlit web application
- **AI**: OpenAI GPT-4o model

## Project Structure

```
pitchslap/
├── app/
│   └── main.py          # FastAPI backend application
├── .env                 # Environment variables (create from .env.example)
├── .env.example         # Template for environment variables
├── Dockerfile           # For deploying to Google Cloud Run
├── deploy.sh            # Deployment script for Google Cloud Run
├── requirements.txt     # Python dependencies
├── streamlit_app.py     # Streamlit frontend application
└── README.md            # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- An OpenAI API key with access to GPT-4o
- Docker (for deployment)
- Google Cloud account (for deployment)

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pitchslap.git
   cd pitchslap
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file from the template:
   ```bash
   cp .env.example .env
   ```

5. Edit the `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   API_URL=http://localhost:8000
   ```

6. Run the FastAPI backend:
   ```bash
   uvicorn app.main:app --reload
   ```

7. In a new terminal, run the Streamlit frontend:
   ```bash
   streamlit run streamlit_app.py
   ```

8. Open your browser and navigate to `http://localhost:8501`

## Deployment

### Google Cloud Run

1. Make sure you have the Google Cloud SDK installed and configured.

2. Run the deployment script:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. The script will build and deploy the FastAPI application to Google Cloud Run and provide you with the service URL.

4. Update the `API_URL` in your `.env` file with the new service URL.

### Streamlit Deployment

You can deploy the Streamlit frontend using Streamlit Sharing:

1. Push your code to a GitHub repository.

2. Visit [Streamlit Sharing](https://share.streamlit.io/) and connect your GitHub repository.

3. Set the required secrets:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `API_URL`: Your Google Cloud Run service URL

## Usage

1. Fill in the form with your requirements:
   - Industry
   - Target Audience
   - Problem to Solve
   - Additional Requirements (optional)
   - Number of Ideas to Generate

2. Click "Generate Ideas" and wait for the AI to work its magic.

3. View the generated ideas and download them as a text file if desired.

## License

MIT

## Acknowledgements

- [OpenAI](https://openai.com/) for the GPT-4o model
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)