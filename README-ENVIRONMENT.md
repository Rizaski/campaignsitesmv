# Environment Variables Setup

## Important Security Note

**Firebase API keys are NOT secret keys** - they are public and meant to be included in client-side code. However, they are restricted by:
- Domain restrictions (configured in Firebase Console)
- API restrictions (which Firebase services can be called)

Using environment variables is still recommended for:
- Managing different configurations for dev/staging/production
- Keeping configuration separate from code
- Easier updates without code changes
- **Not committing credentials to Git**

## Current Setup

The application now uses a separate `firebase-config.js` file that can be generated from environment variables. This means:
- ✅ Credentials are no longer hardcoded in `app.js`
- ✅ Works without environment variables (uses defaults)
- ✅ Can override with environment variables when needed
- ✅ Safe for deployment (no breaking changes)
- ✅ Build script automatically injects environment variables

## Setting Up Environment Variables

### For Local Development

**Option 1: Using Build Script (Recommended)**

1. Set environment variables in your terminal:
   ```bash
   # Windows PowerShell
   $env:VITE_FIREBASE_API_KEY="your_api_key"
   $env:VITE_FIREBASE_AUTH_DOMAIN="your_project.firebaseapp.com"
   # ... etc
   
   # Linux/Mac
   export VITE_FIREBASE_API_KEY="your_api_key"
   export VITE_FIREBASE_AUTH_DOMAIN="your_project.firebaseapp.com"
   # ... etc
   ```

2. Run the build script to generate config:
   ```bash
   node build-config.js
   ```

3. Start your development server:
   ```bash
   python server.py
   ```

**Option 2: Manual Config File**

1. Create `firebase-config.local.js` (this file is gitignored):
   ```javascript
   const firebaseConfig = {
       apiKey: "your_api_key",
       authDomain: "your_project.firebaseapp.com",
       projectId: "your_project_id",
       storageBucket: "your_project.firebasestorage.app",
       messagingSenderId: "your_sender_id",
       appId: "your_app_id",
       measurementId: "your_measurement_id"
   };
   export { firebaseConfig };
   ```

2. Temporarily rename it to `firebase-config.js` (or modify the import in `app.js`)

### For Vercel Deployment

1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add each variable:
   - `VITE_FIREBASE_API_KEY`
   - `VITE_FIREBASE_AUTH_DOMAIN`
   - `VITE_FIREBASE_PROJECT_ID`
   - `VITE_FIREBASE_STORAGE_BUCKET`
   - `VITE_FIREBASE_MESSAGING_SENDER_ID`
   - `VITE_FIREBASE_APP_ID`
   - `VITE_FIREBASE_MEASUREMENT_ID` (optional)

4. Redeploy your application

## Getting Your Firebase Credentials

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Click the gear icon ⚙️ → **Project settings**
4. Scroll down to **Your apps** section
5. Click on your web app (or create one if you haven't)
6. Copy the configuration values

## Security Best Practices

1. **Domain Restrictions**: 
   - In Firebase Console → Authentication → Settings → Authorized domains
   - Add only your production domains
   - Remove localhost for production apps

2. **API Restrictions**:
   - In Google Cloud Console → APIs & Services → Credentials
   - Restrict your API key to only Firebase services

3. **Firestore Rules**:
   - Always review and test your Firestore security rules
   - Never allow public read/write access in production

4. **Storage Rules**:
   - Configure Firebase Storage security rules
   - Restrict access based on authentication

## Troubleshooting

### Environment variables not working?

1. **Check variable names**: Must start with `VITE_` for Vite-based projects
2. **Restart server**: Environment variables are loaded at build/start time
3. **Check syntax**: No spaces around `=` in `.env.local`
4. **Verify file location**: `.env.local` should be in the project root

### Still using default values?

- The app will use default values if environment variables are not set
- This is intentional for backward compatibility
- Check browser console for any errors

## Migration from Hardcoded Values

If you want to completely remove hardcoded values:

1. Set all environment variables in Vercel
2. Update `app.js` to remove the fallback values (optional, not recommended)
3. Test thoroughly before deploying

**Note**: Keeping fallback values is recommended for easier local development and as a safety net.

