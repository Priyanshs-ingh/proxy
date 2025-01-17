from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
import pandas as pd
import requests
import json
from datetime import datetime
import os
import uvicorn
import streamlit as st
from io import StringIO, BytesIO

# ============= INPUT YOUR CREDENTIALS HERE =============
PROXYCURL_API_KEY = "hAyhbZzK1BArkuLhlH0PvA"  # Replace with your actual API key
# ========================================================

def format_date(date_dict):
    if not date_dict:
        return "Present"
    month = str(date_dict.get('month', '')).zfill(2)
    year = str(date_dict.get('year', ''))
    return f"{month}/{year}" if month and year else "N/A"

def fetch_linkedin_data(linkedin_url):
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    headers = {'Authorization': f'Bearer {PROXYCURL_API_KEY}'}

    params = {
        'url': linkedin_url,
        'fallback_to_cache': 'on-error',
        'use_cache': 'if-present',
        'skills': 'include',
        'inferred_salary': 'include',
        'personal_email': 'include',
        'personal_contact_number': 'include',
        'twitter_profile_id': 'include',
        'facebook_profile_id': 'include',
        'github_profile_id': 'include'
    }

    try:
        response = requests.get(
            url=api_endpoint,
            params=params,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        profile_data = {
            'full_name': data.get('full_name', ''),
            'headline': data.get('headline', ''),
            'summary': data.get('summary', ''),
            'country': data.get('country_full_name', ''),
            'city': data.get('city', ''),
            'email': data.get('personal_email', ''),
            'contact_number': data.get('personal_contact_number', ''),
            'github': data.get('github_profile_id', ''),
            'twitter': data.get('twitter_profile_id', ''),
            'facebook': data.get('facebook_profile_id', ''),
            'skills': ", ".join(data.get('skills', [])),
            'educations': [
                {
                    'institution_name': edu.get('school', ''),
                    'degree': edu.get('degree', ''),
                    'field_of_study': edu.get('major', ''),
                    'start_date': format_date(edu.get('starts_at')),
                    'end_date': format_date(edu.get('ends_at'))
                } for edu in data.get('education', [])
            ],
            'experiences': [
                {
                    'title': exp.get('title', ''),
                    'company': exp.get('company', ''),
                    'location': exp.get('location', ''),
                    'description': exp.get('description', ''),
                    'start_date': format_date(exp.get('starts_at')),
                    'end_date': format_date(exp.get('ends_at'))
                } for exp in data.get('experiences', [])
            ]
        }

        return profile_data

    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return None

app = FastAPI()

@app.post("/process")
async def process_csv(file: UploadFile = None, linkedin_url: str = Form(None)):
    results = []

    if file:
        content = await file.read()
        df = pd.read_csv(StringIO(content.decode('utf-8')))
        urls = df.iloc[:, 0].tolist()
    elif linkedin_url:
        urls = [linkedin_url]
    else:
        return {"error": "No input provided."}

    profiles = []
    educations = []
    experiences = []

    for url in urls:
        data = fetch_linkedin_data(url)
        if data:
            profile_dict = {
                "full_name": data["full_name"],
                "headline": data["headline"],
                "summary": data["summary"],
                "country": data["country"],
                "city": data["city"],
                "email": data["email"],
                "contact_number": data["contact_number"],
                "github": data["github"],
                "twitter": data["twitter"],
                "facebook": data["facebook"],
                "skills": data["skills"]
            }
            profile_id = len(profiles) + 1
            profile_dict["profile_id"] = profile_id
            profiles.append(profile_dict)

            for edu in data["educations"]:
                edu["profile_id"] = profile_id
                educations.append(edu)

            for exp in data["experiences"]:
                exp["profile_id"] = profile_id
                experiences.append(exp)

    output_file = f"linkedin_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    pd.DataFrame(profiles).to_excel(writer, sheet_name='Profiles', index=False)
    pd.DataFrame(educations).to_excel(writer, sheet_name='Educations', index=False)
    pd.DataFrame(experiences).to_excel(writer, sheet_name='Experiences', index=False)
    writer.close()
    return FileResponse(output_file, filename=output_file)

# Streamlit UI
def main():
    st.title("LinkedIn Data Scraper")

    st.write("### Upload a CSV of LinkedIn URLs or Enter a Single URL")
    file = st.file_uploader("Upload CSV", type=["csv"])
    linkedin_url = st.text_input("Enter LinkedIn URL")

    if st.button("Process"):
        if not file and not linkedin_url:
            st.error("Please upload a file or enter a URL.")
        else:
            with st.spinner("Processing..."):
                if file:
                    files = {"file": file.getvalue()}
                    response = requests.post("http://127.0.0.1:8000/process", files=files)
                else:
                    data = {"linkedin_url": linkedin_url}
                    response = requests.post("http://127.0.0.1:8000/process", data=data)

                if response.status_code == 200:
                    st.success("Data processed successfully!")
                    st.download_button(
                        "Download Excel", data=response.content, file_name="linkedin_data.xlsx"
                    )
                else:
                    st.error("An error occurred. Please try again.")

if __name__ == "__main__":
    import threading

    def run_fastapi():
        uvicorn.run(app, host="0.0.0.0", port=8000)

    threading.Thread(target=run_fastapi, daemon=True).start()
    main()
