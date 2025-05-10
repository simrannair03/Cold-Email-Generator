# 📧 Cold Email Generator using Generative AI

This project is an intelligent, LLM-powered Streamlit app that helps you generate professional, personalized cold emails for job postings by extracting job metadata and matching it to relevant items in your tech portfolio. It utilizes Groq’s **LLaMA3-70B** via LangChain and includes ChromaDB-based vector search for portfolio matching.

---

## 🚀 Features

- 🔍 Scrape and extract job details from real job posting URLs  
- 🤖 Use LLaMA3 to extract job title, experience, skills, and description  
- 🧠 Match job skills with your portfolio projects using ChromaDB vector search  
- 📬 Generate a professional cold email tailored to the job  
- 💾 Download the email in Markdown format  
- 🧪 Optional test mode for demo without scraping  

---

## 🧰 Technologies Used

- [Python](https://www.python.org/)  
- [Streamlit](https://streamlit.io/)  
- [LangChain](https://www.langchain.com/)  
- [Groq LLaMA3-70B](https://console.groq.com)  
- [ChromaDB](https://docs.trychroma.com/)  
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)  
- [Requests](https://docs.python-requests.org/)  

---

## 📁 Folder Structure

```

📦 cold-email-generator/
┣ 📄 app.py
┣ 📄 my\_portfolio.csv
┣ 📄 requirements.txt
┣ 📄 README.md

````

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cold-email-generator.git
   cd cold-email-generator
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Groq API key**

   * In `app.py`, replace:

     ```python
     groq_api_key='your_groq_api_key_here'
     ```

---

## 📊 Prepare Your Portfolio

Prepare a CSV named `my_portfolio.csv` with at least the following columns:

| Techstack                | Links                                                          |
| ------------------------ | -------------------------------------------------------------- |
| Python, Machine Learning | [https://github.com/you/ml](https://github.com/you/ml)         |
| Web Dev, React, Tailwind | [https://github.com/you/webapp](https://github.com/you/webapp) |

---

## ▶️ How to Run

```bash
streamlit run app.py
```

---

## 🧪 Usage Instructions

1. Enter a job posting URL (e.g., from Nike Careers)
2. Click **Generate Email**
3. View the generated email
4. Download the `.md` version of the email

You can also check **"Use test data"** to simulate the workflow without scraping a live URL.

---

## 🛠 Future Improvements

* Add support for more job platforms like LinkedIn or Indeed
* Store portfolios per user with login support
* Add tone customization (formal/friendly)
* Save email history with version control
---

## 📦 Requirements

Dependencies listed in `requirements.txt`:

```txt
streamlit>=1.32.0
requests>=2.31.0
beautifulsoup4>=4.12.2
lxml>=4.9.3
pandas>=2.2.0
uuid
chromadb>=0.4.24
langchain>=0.1.14
langchain-community>=0.0.27
langchain-groq>=0.0.1
```

Install with:

```bash
pip install -r requirements.txt
```
