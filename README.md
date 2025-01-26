# Alumni Insights Dashboard

## Dashboard Link

https://app.powerbi.com/groups/deecc4a2-74b8-424a-8385-8c86fd0fb7f0/reports/7d8cfe80-b366-44cb-be54-4392ab2e9498/50be6beb80322ed2d756?experience=power-bi&bookmarkGuid=b8b44a997ef16c3f69d9

## Project Overview

This project aims to provide real-time insights and engagement tracking for alumni using a Power BI dashboard. It leverages SQL for efficient data pipelines, Python for automated data processing, and Proxycurl for web scraping LinkedIn data.

A Streamlit app complements the dashboard, enabling users to upload their own CSV files with alumni names and LinkedIn URLs for comprehensive data extraction and analysis.

## Key Features

*   **Real-time alumni insights:** The Power BI dashboard provides up-to-date information on alumni activities, engagement, and trends.
*   **Automated data processing:** Python scripts automate data processing and analytics workflows.
*   **LinkedIn data extraction:** Proxycurl is used to scrape relevant alumni data from LinkedIn.
*   **Streamlit app for custom analysis:** Users can upload their own alumni data for personalized insights.

## Data Pipeline

### 1. Data Acquisition

*   Proxycurl is used to scrape alumni data from LinkedIn, including their current roles, companies, locations, and other relevant information.
*   The scraped data is converted into an Excel file for further processing.

### 2. Data Storage

*   The Excel file is imported into a SQL database for efficient storage and retrieval.

### 3. ETL Operations

*   SQL is used to perform Extract, Transform, Load (ETL) operations, ensuring data quality and consistency.

### 4. Data Analysis

*   Python scripts are used to analyze the data and generate insights.

### 5. Dashboard Visualization

*   Power BI is used to create an interactive dashboard that visualizes the key insights and metrics.

## Streamlit App

The Streamlit app provides a user-friendly interface for custom alumni data analysis. Users can upload their own CSV files containing alumni names and LinkedIn URLs. The app then uses Proxycurl to scrape the corresponding LinkedIn profiles and provides a comprehensive report.

## Technologies Used

*   Power BI
*   SQL
*   Python
*   Proxycurl
*   Streamlit

## Future Enhancements

*   Incorporate additional data sources: Integrate data from other platforms like social media or university databases.
*   Develop predictive analytics: Use machine learning to predict alumni engagement and career trajectories.
*   Enhance the Streamlit app: Add more features and improve the user interface.

## Screenshots

[Include screenshots of your Power BI dashboard and Streamlit app]

## Insights

[Describe some key insights derived from your dashboard]
