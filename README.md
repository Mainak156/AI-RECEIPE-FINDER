# 🍳 AI-Powered Recipe Finder

An interactive AI-based Recipe Generator built with **Streamlit**, **LangChain**, **HuggingFace Embeddings**, **Groq LLM**, and **Chroma Vector Database**.  
This app suggests creative, safe, and culturally contextual recipes based on the ingredients you provide.

---

## 🚀 Features

- Enter comma-separated ingredients  
- AI suggests **multiple safe, creative recipes**  
- Each recipe shows:
  - Step-by-step instructions  
  - Country/cuisine origin  
  - YouTube video search link for recipe tutorials  
- Stores and fetches similar recipes using **Chroma vector database**  
- Uses **Groq's Llama 3-70B** via LangChain for intelligent recipe generation  

---

## 📂 Dataset Source

The recipes are initialized from:

**📖 [Food Ingredients and Recipe Dataset with Image Name Mapping](https://www.kaggle.com/datasets/pes12017000148/food-ingredients-and-recipe-dataset-with-images)**  
- Contains thousands of recipes with ingredients and cooking instructions  
- Used to populate the initial vector database for similarity search  

---

## 🛠️ Tech Stack

- 🐍 Python 3.11  
- 🖥️ Streamlit (UI)  
- 🧠 LangChain  
- 🗂️ Chroma Vector DB  
- 🤖 HuggingFace Sentence Transformers  
- 🔥 Groq API (Llama 3-70B)  
- 📄 Pandas (CSV processing)  
- 🌿 dotenv (for API key management)  

---

## 📝 Project Structure
├── app.py # LangGraph workflow, recipe retrieval, and generation logic  
├── ui.py # Streamlit-based frontend interface  
├── requirements.txt # Python dependencies  
├── Food Ingredients and Recipe Dataset with Image Name Mapping.csv  
└── README.md  

---

## 📦 Installation
**1️⃣ Clone this repo:**  
`git clone https://github.com/your-username/ai-recipe-finder.git`  
`cd ai-recipe-finder`  

**2️⃣ Install dependencies:**  
`pip install -r requirements.txt`  

**3️⃣ Add your Groq API Key in a .env file:**  
`GROQ_API_KEY=gsk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx`  

**4️⃣ Run the app:**  
`streamlit run ui.py`  

---

## 📣 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)  
- [HuggingFace Sentence Transformers](https://www.sbert.net/)  
- [Chroma Vector DB](https://www.trychroma.com/)  
- [Groq API](https://console.groq.com/)  
- [Streamlit](https://streamlit.io/)  
- [Food Ingredients and Recipe Dataset (Kaggle)](https://www.kaggle.com/datasets/pes12017000148/food-ingredients-and-recipe-dataset-with-images)  

---

👨‍🍳 **Made with love for AI foodies!**
