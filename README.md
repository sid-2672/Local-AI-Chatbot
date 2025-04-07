# Local AI Chatbot

## Overview

This is a local AI chatbot built using **Streamlit** and **LangChain**. It allows users to:

- Chat with an AI assistant.
- Upload a **PDF** and analyze its content.
- Retrieve information from **Wikipedia** if needed.
- Save and clear chat history.

## Features

- **Local AI Processing:** No need for an internet connection after setup.
- **PDF Support:** Extracts and analyzes text from PDFs.
- **Wikipedia Integration:** Fetches relevant information when the AI response is insufficient.
- **Multiple AI Models:** Supports **Mistral, LLaMA 3, and TinyLLaMA**.

## Installation:

### 1. Clone the Repository:

  git clone https://github.com/sid-2672/Local-AI-Chatbot.git
  cd Local-AI-Chatbot

### 2. Create a Virtual Environment:

  python -m venv venv
  source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
  
### 3. Install Dependencies:

  pip install -r requirements.txt

4. Run the Chatbot:

  streamlit run Chatbot.py

File Structure:

/Local-AI-Chatbot
│── Chatbot.py              # Main chatbot application
│── requirements.txt        # Dependencies
│── README.md               # Documentation
│── /data                   # (Optional) Folder for saved chat history

Usage

    Run the chatbot and interact with the AI.

    Upload PDFs for content analysis.

    View and save conversation history.

    Change AI models from the sidebar.

Contributing

If you want to improve this chatbot, feel free to fork the repository and submit a pull request.

