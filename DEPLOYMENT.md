# PackCheck Deployment Guide

## Why Not Vercel?

Vercel is **NOT suitable** for this application because:
- Serverless function size limit: 250MB (our dependencies exceed this)
- No support for system-level dependencies (Tesseract OCR)
- No persistent file storage
- Limited support for heavy ML libraries (opencv, scikit-learn)

## Recommended Platforms

### Option 1: Render.com (Recommended - FREE tier available)

#### Advantages:
- Free tier with 750 hours/month
- Supports Docker and native Python builds
- Persistent disk storage
- PostgreSQL database included
- Auto-deployment from GitHub
- System dependencies (Tesseract) supported

#### Deployment Steps:

1. **Create Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Connect Repository**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `packcheck` directory as root

3. **Configure Service**
   - **Name**: packcheck-api
   - **Region**: Oregon (US West)
   - **Branch**: main
   - **Root Directory**: Leave blank (render.yaml handles this)
   - **Environment**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && python app.py`

4. **Add Environment Variables**
   ```
   GEMINI_API_KEY=AIzaSyAXFbcJuDQzKKh14Kn4SVC8nbXjSC54J7c
   SECRET_KEY=<generate-a-secret-key>
   DATABASE_URL=<will-be-auto-populated-if-using-render-postgres>
   DEBUG=False
   PORT=5000
   ```

5. **Add PostgreSQL Database** (Optional)
   - In your Render dashboard, click "New +" → "PostgreSQL"
   - Name: packcheck-db
   - Link it to your web service

6. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (~5-10 minutes)
   - Your API will be live at: `https://packcheck-api.onrender.com`

---

### Option 2: Railway.app (Easier Setup)

#### Advantages:
- $5 free credit monthly
- Extremely simple deployment
- Auto-detects Python
- Built-in PostgreSQL
- Environment variable management

#### Deployment Steps:

1. **Create Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your PackCheck repository
   - Railway will auto-detect Python and use `railway.json`

3. **Add Environment Variables**
   - In project settings → Variables:
   ```
   GEMINI_API_KEY=AIzaSyAXFbcJuDQzKKh14Kn4SVC8nbXjSC54J7c
   SECRET_KEY=<generate-a-secret-key>
   DEBUG=False
   PORT=5000
   ```

4. **Add PostgreSQL** (Optional)
   - Click "New" → "Database" → "PostgreSQL"
   - Railway automatically sets DATABASE_URL

5. **Generate Domain**
   - Go to Settings → Networking
   - Click "Generate Domain"
   - Your API will be live at: `https://<your-app>.up.railway.app`

---

### Option 3: Docker Deployment (Any Platform)

Use the included `Dockerfile` to deploy on:
- Google Cloud Run
- AWS ECS
- DigitalOcean App Platform
- Fly.io

#### Build and Run Locally:
```bash
# Build the Docker image
docker build -t packcheck-api .

# Run the container
docker run -p 5000:5000 \
  -e GEMINI_API_KEY=your_key \
  -e SECRET_KEY=your_secret \
  packcheck-api
```

#### Deploy to Google Cloud Run:
```bash
# Build and push
gcloud builds submit --tag gcr.io/YOUR_PROJECT/packcheck-api

# Deploy
gcloud run deploy packcheck-api \
  --image gcr.io/YOUR_PROJECT/packcheck-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key
```

---

## Environment Variables Reference

Required environment variables for all platforms:

| Variable | Description | Example |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | `AIzaSy...` |
| `SECRET_KEY` | Flask secret key | `your-secret-key` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `PORT` | Port to run on | `5000` |
| `DEBUG` | Debug mode (False for production) | `False` |

---

## Post-Deployment Steps

1. **Test Health Endpoint**
   ```bash
   curl https://your-app-url.com/health
   ```

2. **Test API**
   ```bash
   curl https://your-app-url.com/
   ```

3. **Update Frontend**
   - Update your frontend's API URL to point to the deployed backend
   - Update CORS settings if needed

---

## Troubleshooting

### Tesseract Not Found
- Ensure system packages are installed in build command
- For Render: Build command should include apt-get install
- For Docker: Already handled in Dockerfile

### Database Connection Issues
- Verify DATABASE_URL is set correctly
- Check PostgreSQL is provisioned and running
- Ensure database migrations are run

### Package Size Issues
- Use Docker deployment for full control
- Consider splitting heavy dependencies into separate microservices

---

## Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| Render | 750 hrs/month | $7/month | Production apps |
| Railway | $5 credit/month | Pay as you go | Quick prototypes |
| Vercel | ❌ Not suitable | ❌ Not suitable | ❌ Frontend only |
| Google Cloud Run | 2M requests/month | Pay per request | Scalable apps |

---

## Recommended: Use Render.com

For your project, **Render.com is the best choice** because:
1. ✅ Free tier is generous
2. ✅ Easy setup with render.yaml
3. ✅ Handles all dependencies automatically
4. ✅ Free PostgreSQL database
5. ✅ Auto-deployment from GitHub
