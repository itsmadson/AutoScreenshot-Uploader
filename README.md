# AutoScreenshot-Uploader
A Python tool that automatically captures screenshots every 5 minutes and uploads them to your Dropbox account. This tool runs in the background, starts automatically with your system, and handles internet connection interruptions by retrying the upload once the connection is restored.

Here's a README file for your project along with a suggested name and description:

---

## Features

- Captures screenshots of your screen every 5 minutes.
- Automatically uploads screenshots to a designated Dropbox folder.
- Runs in the background and minimizes without interrupting user activity.
- Automatically adds itself to the startup programs on Windows.
- Handles internet connection issues by queuing screenshots and uploading them when the connection is available.
- Prevents multiple instances from running simultaneously.

## Requirements
Install required Python packages:

bashCopypip install pillow dropbox pywin32 psutil

You'll need to set up a Dropbox API key:

## How to use:
To use this script:
Replace YOUR_ACCESS_TOKEN_HERE with your Dropbox access token
Run the script once manually to test it
The script will automatically add itself to Windows startup
For Dropbox access token:
Go to https://www.dropbox.com/developers
Create a new app
Choose "Scoped access"
Choose "Full Dropbox" access
Name your app
In the settings, find your app's OAuth2 access token
