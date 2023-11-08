import requests
import json

# Define Nexus repository URL and package name
NEXUS_URL = "https://nexus.example.com/repository/my-repo/"
PACKAGE_NAME = "my-package.rpm"

# Send a GET request to retrieve version data
response = requests.get(NEXUS_URL + PACKAGE_NAME + "?describe=versions")

if response.status_code == 200:
    data = json.loads(response.text)
    versions = data.get("items", [])
    
    if versions:
        latest_version = max(versions, key=lambda x: x["version"])
        
        # Download the latest version of the package
        download_url = NEXUS_URL + PACKAGE_NAME + "?version=" + latest_version["version"]
        response = requests.get(download_url)
        
        if response.status_code == 200:
            with open(PACKAGE_NAME, "wb") as f:
                f.write(response.content)
            print("Downloaded the latest version:", latest_version["version"])
        else:
            print("Failed to download the latest version.")
    else:
        print("No versions found in the repository.")
else:
    print("Failed to retrieve version information from the repository.")
