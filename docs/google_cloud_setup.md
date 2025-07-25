# Google Cloud & Firebase Project Setup Guide

This document provides a step-by-step guide for the initial, one-time setup of the required Google Cloud Platform (GCP) and Firebase services for the Sentinel project.

## 1. Create the Firebase Project

This single process creates both the Firebase project and the underlying Google Cloud project.

1.  Go to the [Firebase Console](https://console.firebase.google.com/) and log in with your dedicated project email (e.g., `sentinelinvestapp@gmail.com`).
2.  Click **"Create a project"**.
3.  Enter a unique project name (e.g., `sentinel-invest`).
4.  Disable Google Analytics for the MVP to keep the setup clean.
5.  Click **"Create project"** and wait for it to provision.

## 2. Enable Required Cloud Services

From the Firebase Console dashboard for your new project, enable the following services from the left-hand "Build" menu.

#### 2.1. Enable Firestore Database
1.  Click on **Firestore Database** -> **"Create database"**.
2.  Select **Production mode**.
3.  Choose a location/region (e.g., **`eur3 (frankfurt)`**). This region should be used for all other services.
4.  Click **"Enable"**.

#### 2.2. Enable Authentication
1.  Click on **Authentication** -> **"Get started"**.
2.  Select **"Email/Password"** from the list of sign-in providers.
3.  Enable it and click **"Save"**.

#### 2.3. Enable Hosting
1.  Click on **Hosting** -> **"Get started"**.
2.  Follow the simple on-screen prompts to complete the initial setup.

## 3. Enable Required Google Cloud APIs

For our backend and CI/CD pipeline to function, we must manually enable a few core APIs.

1.  Navigate to the [Google Cloud API Library](https://console.cloud.google.com/apis/library).
2.  Ensure your `sentinel-invest` project is selected at the top.
3.  Search for and **ENABLE** the following APIs one by one:
    -   **Artifact Registry API** (for storing Docker images)
    -   **Cloud Run Admin API** (for deploying the backend)

## 4. Create Service Accounts & Keys

Service accounts are used to give our code and our CI/CD pipeline secure, programmatic access to our cloud project.

#### 4.1. Backend Service Account (for Local Development)
1.  In the GCP Console, go to **IAM & Admin** -> **Service Accounts**.
2.  Click **"+ CREATE SERVICE ACCOUNT"**.
3.  **Name:** `sentinel-backend-local`
4.  **Role:** Grant it the **`Editor`** role for broad access during development.
5.  Click **"Done"**.
6.  Find the new account, click the **⋮** menu -> **Manage keys** -> **ADD KEY** -> **Create new key**.
7.  Choose **JSON** and click **"Create"**. A key file will be downloaded.
8.  Rename this file to `serviceAccountKey.json` and place it in the `/backend` directory.
9.  **CRITICAL:** Ensure `serviceAccountKey.json` is listed in your root `.gitignore` file.

#### 4.2. CI/CD Deployer Service Account
1.  Follow the same steps to create another service account.
2.  **Name:** `github-actions-deployer`
3.  **Roles:** Grant it the following specific roles:
    -   `Cloud Run Admin`
    -   `Firebase Hosting Admin`
    -   `Artifact Registry Writer`
    -   `Service Account User`
4.  Create and download a **JSON** key for this account as well. You will not save this key in the repository.
5.  Go to your Sentinel GitHub repository -> **Settings** -> **Secrets and variables** -> **Actions**.
6.  Create a new repository secret named `GCP_SA_KEY` and paste the entire content of the JSON key file into it.
7.  Create another secret named `GCP_PROJECT_ID` and add your project ID (e.g., `sentinel-invest`).

## 5. Create Artifact Registry Repository

1.  In the GCP Console, navigate to **Artifact Registry**.
2.  Click **"+ CREATE REPOSITORY"**.
3.  **Name:** `sentinel`
4.  **Format:** **Docker**
5.  **Region:** `europe-west3 (Frankfurt)` (or your chosen region).
6.  Click **"CREATE"**.

