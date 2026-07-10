# Apartment Management System - Deployment Guide

## Overview
This guide will help you deploy your Apartment Management System so it can be accessed from anywhere (mobile phones, laptops, etc.).

## Method 1: Local Network Access (Quick Start)

### Step 1: Run the Development Server
Open your terminal/command prompt in the project directory and run:

```bash
python manage.py runserver 0.0.0.0:8000
```

The `0.0.0.0` makes the server accessible from other devices on your network.

### Step 2: Find Your IP Address
- **Windows**: Open Command Prompt and type `ipconfig`
- **Mac/Linux**: Open Terminal and type `ifconfig` or `ip a`

Look for your IPv4 address (usually starts with 192.168.x.x or 10.x.x.x)

### Step 3: Access from Other Devices
On any device connected to the same WiFi network, open a browser and go to:
```
http://YOUR_IP_ADDRESS:8000
```

Example: `http://192.168.1.100:8000`

**Note**: Your computer must stay on and the server must keep running for access to work.

---

## Method 2: Cloud Deployment (Recommended for Permanent Access)

### Option A: PythonAnywhere (Free Tier Available)

1. **Create Account**
   - Go to [pythonanywhere.com](https://www.pythonanywhere.com)
   - Sign up for a free account

2. **Create a Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.10 or later

3. **Upload Your Code**
   - Use the "Files" tab to upload your project
   - Or use git to clone your repository

4. **Configure the Web App**
   - In the Web tab, set:
     - **WSGI configuration file**: Point to your `config/wsgi.py`
     - **Virtualenv**: Create a new virtualenv
     - **Working directory**: Set to your project folder

5. **Install Dependencies**
   - In a Bash console:
   ```bash
   pip install django
   pip install python-dateutil
   ```

6. **Configure ALLOWED_HOSTS**
   - Edit `config/settings.py`
   - Add your PythonAnywhere domain:
   ```python
   ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', '*']
   ```

7. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

8. **Reload Your Web App**
   - Click the "Reload" button in the Web tab

### Option B: Render.com (Free Tier Available)

1. **Create Account**
   - Go to [render.com](https://render.com)
   - Sign up for a free account

2. **Push Your Code to GitHub**
   - Create a GitHub repository
   - Push your code to it

3. **Create a Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt && python manage.py migrate`
     - **Start Command**: `gunicorn config.wsgi:application`

4. **Create requirements.txt**
   Create a file named `requirements.txt` in your project root:
   ```
   Django>=6.0.0
   python-dateutil>=2.8.2
   gunicorn>=21.0.0
   ```

5. **Configure ALLOWED_HOSTS**
   - Edit `config/settings.py`
   - Add your Render domain:
   ```python
   ALLOWED_HOSTS = ['your-app-name.onrender.com', '*']
   ```

### Option C: Railway.app (Free Tier Available)

1. **Create Account**
   - Go to [railway.app](https://railway.app)
   - Sign up for a free account

2. **Deploy from GitHub**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

3. **Configure**
   - Railway will auto-detect Django
   - Set environment variables as needed
   - Add your Railway domain to ALLOWED_HOSTS

---

## Security Considerations

### For Production Deployment:

1. **Change DEBUG to False**
   ```python
   # config/settings.py
   DEBUG = False
   ```

2. **Set a Strong SECRET_KEY**
   ```python
   # Generate a new secret key
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   - Replace the SECRET_KEY in settings.py with the generated one

3. **Set Specific ALLOWED_HOSTS**
   ```python
   # Instead of ['*'], use specific domains
   ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
   ```

4. **Use Environment Variables**
   - Store sensitive data in environment variables
   - Use `python-decouple` or `os.environ` to access them

5. **Enable HTTPS**
   - Most cloud providers offer free SSL certificates
   - Always use HTTPS in production

6. **Database Backup**
   - Regularly backup your database
   - For SQLite, copy the `db.sqlite3` file
   - For cloud deployments, use their backup features

---

## Mobile Access Tips

### Responsive Design
Your system already uses Bootstrap 5, which is mobile-responsive. The interface will automatically adjust to mobile screens.

### PWA (Progressive Web App)
To make it installable on mobile devices:
1. Add a manifest.json file
2. Add service worker
3. This is optional but recommended for better mobile experience

---

## Troubleshooting

### "Invalid HTTP_HOST" Error
- Add the domain/IP to ALLOWED_HOSTS in settings.py

### "CSRF Token Missing" Error
- Ensure you're using POST requests with {% csrf_token %} in forms

### Database Locked Error
- Close any database connections
- Ensure only one instance of the server is running

### Can't Access from Other Devices
- Check firewall settings
- Ensure devices are on the same network
- Verify the server is running with 0.0.0.0:8000

---

## Quick Start Commands

```bash
# Activate virtual environment (if using one)
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install django python-dateutil

# Run migrations
python manage.py migrate

# Run development server (accessible from network)
python manage.py runserver 0.0.0.0:8000

# Create superuser for admin access
python manage.py createsuperuser
```

---

## Support

For issues specific to your deployment platform, check their documentation:
- PythonAnywhere: https://help.pythonanywhere.com/
- Render: https://render.com/docs
- Railway: https://docs.railway.app/
