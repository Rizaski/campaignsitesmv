# Vercel Deployment Guide

This guide explains how to deploy the Campaign Pro application to Vercel.

## Prerequisites

1. A Vercel account (sign up at [vercel.com](https://vercel.com))
2. Firebase project with all services configured
3. Git repository (GitHub, GitLab, or Bitbucket)

## Step 1: Prepare Your Repository

1. Make sure all your files are committed to Git
2. Push your code to GitHub, GitLab, or Bitbucket

## Step 2: Set Up Environment Variables in Vercel

**⚠️ IMPORTANT:** You do NOT upload the `env.example` file! That's just a template. You set variables directly in the Vercel dashboard.

### Option A: Using Vercel Dashboard (Recommended)

1. Go to your Vercel dashboard
2. Select your project (or create a new one)
3. Navigate to **Settings** → **Environment Variables**
4. Click **Add New** for each variable below:

   - **Variable Name**: `VITE_FIREBASE_API_KEY` → **Value**: Your Firebase API Key
   - **Variable Name**: `VITE_FIREBASE_AUTH_DOMAIN` → **Value**: `your-project.firebaseapp.com`
   - **Variable Name**: `VITE_FIREBASE_PROJECT_ID` → **Value**: Your Firebase Project ID
   - **Variable Name**: `VITE_FIREBASE_STORAGE_BUCKET` → **Value**: `your-project.firebasestorage.app`
   - **Variable Name**: `VITE_FIREBASE_MESSAGING_SENDER_ID` → **Value**: Your Messaging Sender ID
   - **Variable Name**: `VITE_FIREBASE_APP_ID` → **Value**: Your Firebase App ID
   - **Variable Name**: `VITE_FIREBASE_MEASUREMENT_ID` → **Value**: Your Measurement ID (optional)

5. For each variable, select which environments to apply it to (Production, Preview, Development)
6. Click **Save** after adding each variable
7. **Important**: After adding all variables, you need to **Redeploy** your project for the changes to take effect

### Option B: Using Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Add environment variables:
   ```bash
   vercel env add VITE_FIREBASE_API_KEY
   vercel env add VITE_FIREBASE_AUTH_DOMAIN
   vercel env add VITE_FIREBASE_PROJECT_ID
   vercel env add VITE_FIREBASE_STORAGE_BUCKET
   vercel env add VITE_FIREBASE_MESSAGING_SENDER_ID
   vercel env add VITE_FIREBASE_APP_ID
   vercel env add VITE_FIREBASE_MEASUREMENT_ID
   ```

## Step 3: Deploy to Vercel

### Option A: Using Vercel Dashboard

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your Git repository
3. Configure the project:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (or leave empty)
   - **Build Command**: Leave empty (static site)
   - **Output Directory**: Leave empty
4. Click **Deploy**

### Option B: Using Vercel CLI

1. Navigate to your project directory
2. Run:
   ```bash
   vercel
   ```
3. Follow the prompts to deploy

## Step 4: Update Firebase Configuration (If Using Environment Variables)

**Note**: Currently, the Firebase configuration is hardcoded in `app.js`. To use environment variables, you would need to:

1. Update `app.js` to read from environment variables:
   ```javascript
   const firebaseConfig = {
       apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
       authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
       projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
       storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
       messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
       appId: import.meta.env.VITE_FIREBASE_APP_ID,
       measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID
   };
   ```

2. Or use a build-time replacement script

## Step 5: Configure Custom Domain (Optional)

1. Go to your project settings in Vercel
2. Navigate to **Domains**
3. Add your custom domain
4. Follow the DNS configuration instructions

## Step 6: Set Up Continuous Deployment

Vercel automatically deploys when you push to your main branch. For other branches:

1. Go to **Settings** → **Git**
2. Configure branch deployments
3. Set production branch (usually `main` or `master`)

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_FIREBASE_API_KEY` | Firebase API Key | Yes |
| `VITE_FIREBASE_AUTH_DOMAIN` | Firebase Auth Domain | Yes |
| `VITE_FIREBASE_PROJECT_ID` | Firebase Project ID | Yes |
| `VITE_FIREBASE_STORAGE_BUCKET` | Firebase Storage Bucket | Yes |
| `VITE_FIREBASE_MESSAGING_SENDER_ID` | Firebase Messaging Sender ID | Yes |
| `VITE_FIREBASE_APP_ID` | Firebase App ID | Yes |
| `VITE_FIREBASE_MEASUREMENT_ID` | Firebase Measurement ID (Analytics) | No |

## Troubleshooting

### Build Fails

- Check that all environment variables are set
- Verify Firebase configuration values are correct
- Check Vercel build logs for specific errors

### Firebase Connection Issues

- Verify environment variables are correctly set in Vercel
- Check Firebase project settings
- Ensure Firebase services (Auth, Firestore, Storage) are enabled

### Routing Issues

- The `vercel.json` file includes rewrites for client-side routing
- Ensure all routes point to `index.html` for SPA behavior

## Security Notes

- Never commit `.env.local` or `.env` files to Git
- Environment variables in Vercel are encrypted at rest
- Use different Firebase projects for development and production
- Review Firebase security rules before deploying

## Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Firebase Documentation](https://firebase.google.com/docs)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)

