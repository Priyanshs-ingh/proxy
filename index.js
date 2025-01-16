const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));
const fs = require('fs');
const path = require('path');

// Set your Proxycurl API key
const API_KEY = 'EYMcS6u2HXp61TRA6VuMEw';
const API_ENDPOINT = 'https://nubela.co/proxycurl/api/v2/linkedin';

// Function to fetch LinkedIn profile data
const fetchLinkedInProfile = async (profileUrl) => {
  try {
    const response = await fetch(`${API_ENDPOINT}?url=${encodeURIComponent(profileUrl)}&fallback_to_cache=on&use_cache=if-present&skills=include`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${API_KEY}`
      }
    });

    if (response.ok) {
      return await response.json();
    } else {
      console.error(`Failed to fetch data for ${profileUrl}. Status code: ${response.status}`);
      return null;
    }
  } catch (error) {
    console.error(`Error fetching data for ${profileUrl}:`, error);
    return null;
  }
};

// Function to save data to a CSV file
const saveToCsv = (data, filename) => {
  if (!data || data.length === 0) {
    console.error('No data to save.');
    return;
  }

  const keys = Array.from(new Set(data.flatMap(profile => Object.keys(profile))));
  const csvRows = [keys.join(','), ...data.map(profile => keys.map(key => JSON.stringify(profile[key] || '')).join(','))];

  fs.writeFileSync(path.resolve(filename), csvRows.join('\n'), 'utf-8');
  console.log(`Data has been saved to ${filename}`);
};

// Main function
const main = async () => {
  const linkedinUrls = [
    // Replace with actual LinkedIn profile URLs
    'https://www.linkedin.com/in/pratyaksh-saluja/'
  ];

  const profilesData = [];
  for (const url of linkedinUrls) {
    console.log(`Fetching data for ${url}...`);
    const profileData = await fetchLinkedInProfile(url);
    if (profileData) {
      profilesData.push(profileData);
    }
  }

  saveToCsv(profilesData, 'linkedin_profiles.csv');
};

main().catch(console.error);
