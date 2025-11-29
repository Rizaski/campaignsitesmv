# How to Set Environment Variables

## Important: `env.example` is Just a Template!

The `env.example` file is **NOT** the actual environment variables file. It's just a template showing what variables you need.

## For Vercel Deployment

**You do NOT upload any file to Vercel!** Instead, you set environment variables directly in the Vercel dashboard:

### Step-by-Step Instructions:

1. **Go to Vercel Dashboard**
   - Visit [vercel.com](https://vercel.com)
   - Login to your account

2. **Select Your Project**
   - Click on your project name
   - Or create a new project if you haven't deployed yet

3. **Navigate to Settings**
   - Click on **Settings** in the top menu
   - Click on **Environment Variables** in the left sidebar

4. **Add Each Variable**
   Click **Add New** for each variable below and enter:
   
   | Variable Name | Value (Your Firebase Config) |
   |--------------|------------------------------|
   | `VITE_FIREBASE_API_KEY` | Your Firebase API Key |
   | `VITE_FIREBASE_AUTH_DOMAIN` | `your-project.firebaseapp.com` |
   | `VITE_FIREBASE_PROJECT_ID` | Your Firebase Project ID |
   | `VITE_FIREBASE_STORAGE_BUCKET` | `your-project.firebasestorage.app` |
   | `VITE_FIREBASE_MESSAGING_SENDER_ID` | Your Messaging Sender ID |
   | `VITE_FIREBASE_APP_ID` | Your Firebase App ID |
   | `VITE_FIREBASE_MEASUREMENT_ID` | Your Measurement ID (optional) |

5. **Select Environments**
   - Check **Production**, **Preview**, and **Development** (or just Production)
   - Click **Save**

6. **Redeploy**
   - Go to **Deployments** tab
   - Click the three dots (⋯) on the latest deployment
   - Click **Redeploy**
   - Or push a new commit to trigger automatic deployment

### Where to Find Your Firebase Values:

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Click the gear icon ⚙️ → **Project settings**
4. Scroll down to **Your apps** section
5. Click on your web app (or create one)
6. Copy the values from the config object

Example:
```javascript
const firebaseConfig = {
  apiKey: "AIzaSy...",           // ← VITE_FIREBASE_API_KEY
  authDomain: "xxx.firebaseapp.com", // ← VITE_FIREBASE_AUTH_DOMAIN
  projectId: "xxx",              // ← VITE_FIREBASE_PROJECT_ID
  storageBucket: "xxx.appspot.com", // ← VITE_FIREBASE_STORAGE_BUCKET
  messagingSenderId: "123456789", // ← VITE_FIREBASE_MESSAGING_SENDER_ID
  appId: "1:123:web:abc",        // ← VITE_FIREBASE_APP_ID
  measurementId: "G-XXXXX"       // ← VITE_FIREBASE_MEASUREMENT_ID
};
```

## For Local Development

If you want to use environment variables locally:

1. **Create `.env.local` file** (with the dot at the start)
   ```bash
   # Windows
   copy env.example .env.local
   
   # Mac/Linux
   cp env.example .env.local
   ```

2. **Edit `.env.local`** and replace the placeholder values with your actual Firebase config

3. **Run the build script** before starting your server:
   ```bash
   node build-config.js
   ```

4. **Start your server**:
   ```bash
   python server.py
   ```

**Note:** The `.env.local` file is gitignored, so it won't be committed to your repository.

## Quick Reference

- ✅ **Vercel**: Set variables in Dashboard → Settings → Environment Variables
- ✅ **Local**: Create `.env.local` file (gitignored)
- ❌ **Don't**: Upload `env.example` anywhere - it's just documentation
- ❌ **Don't**: Commit `.env.local` to Git

## Troubleshooting

**Q: Do I need to upload env.example to Vercel?**  
A: No! Vercel doesn't use files for environment variables. You set them in the dashboard.

**Q: Why isn't my config updating?**  
A: Make sure you redeployed after adding environment variables. Vercel needs to rebuild.

**Q: Can I use the same values for all environments?**  
A: Yes, but it's better to use different Firebase projects for dev/staging/production.

