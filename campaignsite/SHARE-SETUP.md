# Enable Voter Database Share Links

Share links use a **client-only** flow: when you create a link, a snapshot of the voter list is stored in Firestore (`sharedVoterSnapshots`). Recipients open the link, enter the temporary password, and the list loads directly from Firestore in the browser—**no backend API or server config is required** for viewing the list. It works the same locally and when deployed (e.g. Vercel).

**You only need the steps below if** you used the older API-based share and see "Share feature is not configured on the server" on a deployed site.

---

## Deployed on Vercel (only if using legacy API share)

If the message appears on your **deployed** URL (e.g. `https://your-app.vercel.app`):

1. **Get your Firebase service account JSON** (same project as your app):
   - [Firebase Console](https://console.firebase.google.com/) → your project → **Project settings** (gear) → **Service accounts** → **Generate new private key** → download the JSON file.

2. **Add it in Vercel:**
   - [Vercel Dashboard](https://vercel.com/dashboard) → your project → **Settings** → **Environment Variables**.
   - **Name:** `FIREBASE_SERVICE_ACCOUNT_JSON`
   - **Value:** Paste the **entire** contents of the JSON file (all keys: `type`, `project_id`, `private_key_id`, `private_key`, `client_email`, etc.). You can paste as one line or multiple lines; both work.
   - Apply to **Production** (and Preview if you use it), then save.

3. **Redeploy** so the new variable is used:
   - **Deployments** → open the **⋯** on the latest deployment → **Redeploy** (or push a new commit and let Vercel deploy).

**Troubleshooting (still "not configured" after the above):**
- Confirm the variable name is exactly `FIREBASE_SERVICE_ACCOUNT_JSON` (no typo, no space).
- The value must be valid JSON. If you wrapped it in extra quotes, remove them.
- After changing env vars you must redeploy; the current deployment was built without the variable.

---

## Local development (Python server)

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

When the app is deployed to **Vercel**, the share API runs as serverless functions under `/api/share/verify`, `/api/share/voters`, and `/api/share/pledge`. Sessions are stored in Firestore (`shareSessions` collection). Use the **"Deployed on Vercel"** section at the top of this doc to configure the env var and redeploy.
