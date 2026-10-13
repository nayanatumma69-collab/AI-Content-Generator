# 🤖 AI Content Generator

## 📌 Project Overview

The **AI Content Generator** is a web-based application built using Python, Streamlit, and the Groq API. It generates AI-powered content based on user instructions and allows users to refine existing content to improve its quality, clarity, tone, and readability.

The application provides an interactive interface where users can select content settings, generate text, analyze content metrics, and refine the generated output.

## 🚀 Live Demo

**Try the application here:**

👉 [AI Content Generator – Live App](https://ai-content-generator-kkwzg66gdmwsswxj4dsfs2.streamlit.app/)

## ⚙️ How It Works

The application follows these steps:

1. **User Input:** The user provides a topic or prompt and selects the required content settings.
2. **Prompt Construction:** The application prepares a structured prompt based on the user's instructions.
3. **AI Content Generation:** The Groq API uses the `openai/gpt-oss-20b` model to generate content.
4. **Content Analysis:** The application calculates content metrics, such as word count, character count, and sentence count.
5. **Content Refinement:** Users can refine the generated text to improve its quality according to their requirements.
6. **Regeneration:** Users can generate fresh content when they need an alternative version.

## ✨ Key Features

- AI-powered content generation.
- Customizable content settings and instructions.
- Content refinement and improvement.
- Content analytics, including word, character, and sentence counts.
- Option to regenerate content.
- Interactive user interface built with Streamlit.
- Integration with the Groq API for language model inference.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Frontend / Web Framework:** Streamlit
- **AI API:** Groq API
- **Language Model:** `openai/gpt-oss-20b`
- **Libraries:** `groq`, `streamlit`, `re`

## 📂 Project Structure

```text
ai-content-generator/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

- **app.py:** Contains the Streamlit interface, content generation logic, content metrics, and refinement functionality.
- **requirements.txt:** Lists the Python dependencies required to run the application.
- **README.md:** Provides project documentation and setup instructions.
- **.gitignore:** Prevents selected local and sensitive files from being committed to GitHub.

## 💻 Installation and Setup

### Prerequisites

- Python 3.9 or later
- A Groq API key
- Git (optional, for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-content-generator.git
cd ai-content-generator
```

Replace `YOUR_USERNAME` with your GitHub username.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure the Groq API Key

Configure your API key using Streamlit Secrets. Create a `.streamlit/secrets.toml` file locally with the following content:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

Replace the placeholder with your own Groq API key. Never upload this file or expose your API key in a public repository.

### Step 4: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## ☁️ Deployment

The application is deployed using **Streamlit Community Cloud** and connected to the GitHub repository.

Live application: [https://ai-content-generator-kkwzg66gdmwsswxj4dsfs2.streamlit.app/](https://ai-content-generator-kkwzg66gdmwsswxj4dsfs2.streamlit.app/)

## ⚠️ Limitations and Responsible Use

- AI-generated content may contain inaccurate or misleading information.
- Review and verify generated content before using it for important or professional purposes.
- Content quality depends on the input prompt and the language model's response.
- A valid Groq API key and API availability are required for content generation.
- Do not submit confidential or sensitive information in prompts.

## 🎯 Learning Outcomes

This project demonstrates practical experience with:

- Integrating a large language model through an API.
- Building an interactive AI application using Streamlit.
- Prompt engineering for content generation.
- Processing and analyzing generated text.
- Implementing an AI-powered content refinement workflow.
- Managing API credentials securely for deployment.

## 👩‍💻 Author

Developed as part of an Artificial Intelligence learning and project portfolio to demonstrate practical skills in Python, Generative AI, prompt engineering, and application development.
