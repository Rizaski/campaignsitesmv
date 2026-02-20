# Enable Voter Database Share Links

The **Share voter database** feature (temporary password links) needs the server to connect to Firebase. If you see "Share feature is not configured on the server", do the following.

**Required:** Install the Firebase Admin SDK (once per Python environment):
```bash
pip install firebase-admin
```
If you use a specific Python (e.g. from start-server.ps1), run:
```bash
"C:\Users\Empower\AppData\Local\Programs\Python\Python313\python.exe" -m pip install firebase-admin
```

## 1. Get a Firebase Service Account Key

1. Open [Firebase Console](https://console.firebase.google.com/) and select the **same project** your app uses (e.g. `version6-7c39b` from your app’s Firebase config).
2. Go to **Project settings** (gear) → **Service accounts**.
3. Click **Generate new private key** and confirm. A JSON file will download.

## 2. Add the Key on the Server

1. Rename or copy the downloaded JSON file to:
   ```
   campaignsite/serviceAccountKey.json
   ```
   So the file path is:
   - From repo root: `campaignsite/serviceAccountKey.json`
   - Full path example: `d:\CampaignSite\campaignsite\serviceAccountKey.json`

2. **Do not commit this file** to git (it contains secrets). Add to `.gitignore`:
   ```
   campaignsite/serviceAccountKey.json
   ```

## 3. Restart the Server

Restart the Python server. On startup you should see:

```
Share API: enabled (Firebase connected).
```

Share links and the temporary password screen will then work.

## Alternative: Environment Variable

Instead of placing the key in `campaignsite/serviceAccountKey.json`, you can set:

- **Windows (PowerShell):**  
  `$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\your-service-account-key.json"`
- **Linux/macOS:**  
  `export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account-key.json"`

Then run the server from that same terminal. The server will use this key when the file above is not present.

---

## Deployed on Vercel

When the app is deployed to **Vercel**, the share API runs as serverless functions under `/api/share/verify`, `/api/share/voters`, and `/api/share/pledge`. Sessions are stored in Firestore in the `shareSessions` collection (no in-memory state).

1. In the [Vercel dashboard](https://vercel.com/dashboard), open your project → **Settings** → **Environment Variables**.
2. Add a variable:
   - **Name:** `FIREBASE_SERVICE_ACCOUNT_JSON`
   - **Value:** The **entire contents** of your Firebase service account JSON file (the same project as your app, e.g. `version6-7c39b`). Paste the whole JSON as a single line or multi-line string.
3. Redeploy the project so the new variable is applied.

After that, share links and the temporary password screen will work on your Vercel URL.
