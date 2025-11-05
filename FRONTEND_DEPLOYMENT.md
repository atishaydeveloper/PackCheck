# PackCheck Frontend Deployment Guide

Your backend API is already live at: **https://packcheck-v1.onrender.com**

Now you need to deploy your frontend (React website).

## Quick Start: View Your Website Locally

1. **Navigate to frontend directory:**
   ```bash
   cd packcheck/frontend
   ```

2. **Install dependencies (if not already installed):**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser to:**
   ```
   http://localhost:5173
   ```

Your website will now be running locally and connected to your deployed backend API!

---

## Deploy Frontend to Vercel (Recommended - FREE)

Vercel is perfect for React/Vite frontends and has a generous free tier.

### Option A: Deploy via Vercel Dashboard (Easiest)

1. **Go to [vercel.com](https://vercel.com)**
2. **Sign up/Login** with GitHub
3. **Click "Add New" → "Project"**
4. **Import your GitHub repository** (atishaydeveloper/PackCheck)
5. **Configure the project:**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Install Command:** `npm install`

6. **Add Environment Variable:**
   - Click "Environment Variables"
   - Add: `VITE_API_URL` = `https://packcheck-v1.onrender.com`

7. **Click "Deploy"**
8. **Wait 2-3 minutes** for deployment to complete
9. **Your website will be live!** at something like: `https://packcheck.vercel.app`

### Option B: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend directory
cd packcheck/frontend

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? packcheck-frontend
# - Directory? ./ (current directory)
# - Override settings? No

# Set environment variable
vercel env add VITE_API_URL
# Enter: https://packcheck-v1.onrender.com
# Select: Production
```

---

## Alternative: Deploy to Netlify (Also FREE)

### Deploy via Netlify Dashboard

1. **Go to [netlify.com](https://netlify.com)**
2. **Sign up/Login** with GitHub
3. **Click "Add new site" → "Import an existing project"**
4. **Connect to GitHub** and select your repository
5. **Configure build settings:**
   - **Base directory:** `frontend`
   - **Build command:** `npm run build`
   - **Publish directory:** `frontend/dist`

6. **Add Environment Variable:**
   - Go to Site Settings → Environment Variables
   - Add: `VITE_API_URL` = `https://packcheck-v1.onrender.com`

7. **Click "Deploy site"**
8. **Your website will be live!** at something like: `https://packcheck.netlify.app`

---

## Alternative: Deploy to Render (Same Platform as Backend)

This keeps both frontend and backend on the same platform.

1. **Go to [render.com](https://render.com)**
2. **Click "New +" → "Static Site"**
3. **Connect your GitHub repository**
4. **Configure:**
   - **Name:** packcheck-frontend
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Publish Directory:** `frontend/dist`

5. **Add Environment Variable:**
   - Key: `VITE_API_URL`
   - Value: `https://packcheck-v1.onrender.com`

6. **Create Static Site**

---

## Important: Update Frontend Configuration

The configuration has already been updated for you:

✅ Created `frontend/.env` with production API URL
✅ Created `frontend/src/config.js` for API configuration
✅ Updated `AlternativesDialog.jsx` to use config

**You need to check and update ALL other API calls in your code.**

### Find all API calls that need updating:

```bash
cd packcheck/frontend
grep -r "axios\|fetch" src --include="*.jsx" --include="*.js"
```

Replace all hardcoded `http://localhost:5000` with `API_URL` from config.

---

## Build Your Frontend Locally (Optional)

To test the production build locally:

```bash
cd packcheck/frontend

# Build for production
npm run build

# Preview the production build
npm run preview
```

Then visit: `http://localhost:4173`

---

## Summary

**Backend (API):** ✅ Already deployed at https://packcheck-v1.onrender.com

**Frontend (Website):** Choose ONE of these:
1. ⭐ **Vercel** (Recommended) - Best for React/Vite
2. 🌐 **Netlify** - Also excellent for static sites
3. 🎨 **Render** - Keep everything in one place

**Estimated deployment time:** 2-5 minutes

After deployment, your full-stack PackCheck application will be live! 🎉

---

## Troubleshooting

### CORS Errors
If you see CORS errors, your backend is already configured with:
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```
This should work. If issues persist, update to allow your frontend domain specifically.

### API Not Connecting
1. Check browser console for errors
2. Verify `VITE_API_URL` environment variable is set correctly
3. Make sure backend is running: https://packcheck-v1.onrender.com/health

### Build Errors
1. Make sure all dependencies are installed: `npm install`
2. Check for TypeScript errors: `npm run lint`
3. Try deleting `node_modules` and reinstalling

---

## Next Steps After Deployment

1. ✅ Test all features on the live site
2. ✅ Update your README with live URLs
3. ✅ Share your deployed application!
4. ✅ Set up custom domain (optional)
