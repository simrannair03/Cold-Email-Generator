import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import json
import chromadb
import pandas as pd
import uuid
import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup

# Initialize LLM
try:
    llm = ChatGroq(
        temperature=0,
        groq_api_key='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',
        model_name="llama3-70b-8192"
    )
except Exception as e:
    st.error(f"LLM initialization failed: {str(e)}")
    st.stop()

def load_job_data(url):
    """Alternative web scraping function that bypasses WebBaseLoader issues"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Use lxml parser which is more forgiving than html.parser
        soup = BeautifulSoup(response.text, "lxml")
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        st.error(f"Failed to load job page: {str(e)}")
        return None

def load_portfolio():
    """Load portfolio data from CSV into ChromaDB"""
    csv_path = Path('my_portfolio.csv')
    if not csv_path.exists():
        st.error(f"Portfolio CSV not found at: {csv_path.absolute()}")
        return None
    
    try:
        df = pd.read_csv(csv_path)
        client = chromadb.PersistentClient('vectorstore')
        collection = client.get_or_create_collection(name="portfolio")
        
        if not collection.count():
            for _, row in df.iterrows():
                collection.add(
                    documents=row["Techstack"],
                    metadatas={"links": row["Links"]},
                    ids=[str(uuid.uuid4())]
                )
        return collection
    except Exception as e:
        st.error(f"Failed to load portfolio: {str(e)}")
        return None

def extract_job_info(page_content):
    """Extract job details from webpage content"""
    if not page_content:
        return None
        
    try:
        prompt_extract = PromptTemplate.from_template("""
        ### WEBPAGE CONTENT:
        {page_data}
        
        ### TASK:
        Extract exactly these fields as VALID JSON:
        {{
            "role": "<job_title>",
            "experience": "<years_requirements>",
            "skills": ["<skill1>", "<skill2>"],
            "description": "<job_summary>"
        }}
        
        ### RULES:
        - Return ONLY the JSON object
        - No additional text/comments
        - Empty array for skills if none found
        - Empty strings for missing fields
        """)
        
        chain = prompt_extract | llm
        response = chain.invoke({'page_data': page_content})
        
        # Clean and validate JSON response
        json_str = response.content.strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
        
        if not json_str or not json_str.startswith("{"):
            st.error(f"Invalid JSON format received: {json_str[:100]}...")
            return None
            
        return json.loads(json_str)
        
    except json.JSONDecodeError:
        st.error("The AI returned invalid JSON format")
        return None
    except Exception as e:
        st.error(f"Extraction error: {str(e)}")
        return None

def generate_email(job_info, links):
    """Generate cold email from job info and portfolio links"""
    if not job_info:
        return "Error: No valid job information provided"
    
    try:
        prompt_email = PromptTemplate.from_template("""
        ### JOB DETAILS:
        {job_info}
        
        ### RELEVANT PORTFOLIO:
        {links}
        
        ### INSTRUCTIONS:
        Write a professional email as Mohan (BDE at AtliQ):
        1. Start with personalized greeting
        2. Highlight relevant experience (match skills: {skills})
        3. Include 1-2 portfolio examples
        4. Keep concise (3 paragraphs max)
        5. Professional closing
        
        ### EMAIL:
        """)
        
        response = (prompt_email | llm).invoke({
            "job_info": json.dumps(job_info, indent=2),
            "links": json.dumps(links, indent=2),
            "skills": ", ".join(job_info.get('skills', []))
        })
        
        return response.content
    except Exception as e:
        return f"Email generation failed: {str(e)}"

def main():
    st.set_page_config(
        page_title="Job Email Generator",
        page_icon="📧",
        layout="wide"
    )
    
    st.title("📧 Job Email Generator")
    st.markdown("Generate personalized outreach emails for job postings")
    
    with st.expander("⚙️ Settings", expanded=False):
        url = st.text_input(
            "Job URL",
            value="https://jobs.nike.com/job/R-33460",
            help="Paste a URL from Nike's careers page"
        )
        test_mode = st.checkbox("Use test data", help="Bypass web scraping for testing")
    
    if st.button("✨ Generate Email", type="primary"):
        with st.spinner("Processing job posting..."):
            try:
                # Load data
                if test_mode:
                    page_content = None
                    job_info = {
                        "role": "3D Footwear Designer II",
                        "experience": "5+ years in footwear design",
                        "skills": ["CAD", "3D Modeling", "Prototyping"],
                        "description": "Design innovative footwear products using 3D tools"
                    }
                    # st.success("Using test data - bypassing web scraping")
                else:
                    page_content = load_job_data(url)
                    if not page_content:
                        st.error("Failed to load job page content")
                        return
                    
                    job_info = extract_job_info(page_content)
                    if not job_info:
                        return
                
                # Display extracted info
                # with st.expander("🔍 Extracted Job Details", expanded=True):
                    # st.json(job_info)
                
                # Get relevant portfolio links
                portfolio = load_portfolio()
                links = []
                if portfolio and job_info.get('skills'):
                    links = portfolio.query(
                        query_texts=job_info['skills'],
                        n_results=2
                    ).get('metadatas', [])
                
                # Generate and display email
                email_content = generate_email(job_info, links)
                
                st.divider()
                st.subheader("✉️ Generated Email")
                st.markdown(email_content)
                
                # Add download option
                st.download_button(
                    label="📥 Download Email",
                    data=email_content,
                    file_name=f"nike_email_{job_info.get('role','').replace(' ','_')}.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    # Install required packages if missing
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        import subprocess
        subprocess.run(["pip", "install", "lxml", "beautifulsoup4"], check=True)
    
    main()