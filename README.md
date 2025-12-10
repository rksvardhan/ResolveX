# 🎓 Complaint Management System (Django)

A comprehensive web-based complaint management system built with Django, designed for educational institutions to efficiently handle and track student complaints and grievances.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Integration](#api-integration)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The Complaint Management System is a robust Django-based web application that streamlines the process of handling complaints in educational institutions. It provides a user-friendly interface for students to submit complaints and for administrators to manage and track them efficiently.

### Key Highlights

- **AI-Powered Analysis**: Integrated with Google Gemini AI for intelligent complaint analysis and priority assignment
- **Role-Based Access**: Separate dashboards for students and grievance members
- **Real-time Tracking**: Live status updates and progress tracking
- **PDF Generation**: Automatic complaint report generation
- **Modern UI**: Material Design-based responsive interface
- **Security**: Comprehensive security measures and data protection

## ✨ Features

### For Students
- **User Registration & Authentication**: Secure account creation with email verification
- **Complaint Submission**: Easy-to-use form for submitting complaints with AI-powered priority assignment
- **Complaint Tracking**: Real-time status updates (Pending, In Progress, Resolved)
- **Dashboard**: Personal dashboard with complaint statistics and management
- **PDF Export**: Download complaint details as PDF reports
- **Profile Management**: Update personal information and contact details
- **Dual Chatbot System**: 
  - **IBM Watson Assistant**: Enterprise-grade chatbot for general assistance and support
  - **AI-Powered Chatbot**: Google Gemini AI for intelligent conversation and complaint guidance

### For Grievance Members/Administrators
- **Complaint Management**: View, filter, and manage all complaints
- **Status Updates**: Update complaint status and send notifications
- **Analytics Dashboard**: Comprehensive statistics and reporting
- **Search & Filter**: Advanced search and filtering capabilities
- **Bulk Operations**: Handle multiple complaints efficiently
- **AI Analysis**: Leverage AI insights for better decision making

### System Features
- **AI Integration**: Google Gemini AI for complaint analysis and priority assignment
- **Email Notifications**: Automated email alerts for status changes
- **Responsive Design**: Mobile-friendly interface
- **Security**: CSRF protection, secure sessions, and data validation
- **Multi-College Support**: Support for multiple educational institutions
- **Branch Management**: Department-wise complaint categorization

## 🛠 Tech Stack

### Backend
- **Django 3.2.2** - Web framework
- **Python 3.x** - Programming language
- **PostgreSQL** - Database
- **psycopg2-binary** - PostgreSQL adapter

### Frontend
- **Bootstrap 5** - CSS framework
- **Material Design** - UI components
- **jQuery** - JavaScript library
- **Chart.js** - Data visualization
- **Crispy Forms** - Form rendering

### AI & External Services
- **Google Gemini AI** - Complaint analysis, priority assignment, and AI chatbot
- **IBM Watson Assistant** - Enterprise-grade conversational AI chatbot
- **ReportLab** - PDF generation
- **Django Allauth** - Authentication system

### Additional Libraries
- **Django Extensions** - Development tools
- **Django Suit** - Admin interface enhancement
- **Pillow** - Image processing
- **python-dotenv** - Environment variable management

## 📁 Project Structure

```
ComplaintManagement-Django/
├── ComplaintMS/                    # Main Django app
│   ├── migrations/                 # Database migrations
│   ├── static/ComplaintMS/         # Static files (CSS, JS, images)
│   │   ├── css/                   # Stylesheets
│   │   ├── js/                    # JavaScript files
│   │   ├── img/                   # Images and icons
│   │   └── scss/                  # SCSS source files
│   ├── templates/ComplaintMS/      # HTML templates
│   ├── models.py                  # Database models
│   ├── views.py                   # View functions
│   ├── urls.py                    # URL patterns
│   ├── forms.py                   # Django forms
│   ├── admin.py                   # Admin configuration
│   └── ai_service.py              # AI integration service
├── web/                           # Django project settings
│   ├── settings.py               # Main settings
│   ├── urls.py                   # Root URL configuration
│   └── wsgi.py                   # WSGI configuration
├── static/                        # Global static files
├── templates/                     # Global templates
├── venv/                         # Virtual environment
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- PostgreSQL 12 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd ComplaintManagement-Django
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup
1. Create a PostgreSQL database named `complaintmsdjango`
2. Update database credentials in `web/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'complaintmsdjango',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 7: Run the Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Database Configuration
DB_NAME=complaintmsdjango
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432

# Email Configuration
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com

# AI Configuration
GEMINI_API_KEY=your_gemini_api_key

# Security
SECRET_KEY=your_secret_key
DEBUG=True
```

### Email Configuration
Update email settings in `web/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
```

### AI Integration
1. Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add the API key to your `.env` file or `settings.py`:

```python
GEMINI_API_KEY = 'your_gemini_api_key'
```

## 📱 Usage

### Student Workflow
1. **Register**: Create an account with personal details
2. **Login**: Access the student dashboard
3. **Submit Complaint**: Fill out the complaint form with AI-powered priority assignment
4. **Track Status**: Monitor complaint progress in real-time
5. **Download Reports**: Export complaint details as PDF

### Administrator Workflow
1. **Login**: Access the admin dashboard
2. **View Complaints**: See all pending and in-progress complaints
3. **Update Status**: Change complaint status and send notifications
4. **Analytics**: Review complaint statistics and trends
5. **Manage Users**: Handle user accounts and permissions

### AI Features
- **Automatic Priority Assignment**: AI analyzes complaint content and assigns appropriate priority levels
- **Smart Analysis**: Provides insights and recommendations for complaint handling
- **Dual Chatbot System**:
  - **IBM Watson Assistant**: Enterprise-grade chatbot for general assistance and support
  - **AI-Powered Chatbot**: Google Gemini AI for intelligent conversation and complaint guidance

## 🤖 API Integration

### Google Gemini AI
The system integrates with Google Gemini AI for:
- Complaint content analysis
- Priority level assignment
- Intelligent insights and recommendations
- AI-powered chatbot responses

### IBM Watson Assistant
The system also integrates with IBM Watson Assistant for:
- Enterprise-grade conversational AI
- General assistance and support
- Advanced natural language processing
- Scalable chatbot infrastructure

### Email Notifications
- Status change notifications
- Password reset emails
- Account activation emails
- System alerts

## 📊 Database Schema

### Models
- **User**: Django's built-in user model
- **Profile**: Extended user profile with college and branch information
- **Complaint**: Main complaint model with AI analysis and priority
- **Grievance**: Grievance member model

### Key Fields
- Complaint status tracking (Pending, In Progress, Resolved)
- Priority levels (Low, Medium, High, Urgent)
- AI analysis and recommendations
- Timestamp tracking
- User association

## 🔒 Security Features

- **CSRF Protection**: Cross-site request forgery protection
- **Secure Sessions**: HTTP-only and secure session cookies
- **Password Validation**: Strong password requirements
- **SQL Injection Prevention**: Django ORM protection
- **XSS Protection**: Content Security Policy headers
- **HTTPS Support**: SSL/TLS encryption ready

## 🎨 UI/UX Features

- **Material Design**: Modern, intuitive interface
- **Responsive Layout**: Mobile-friendly design
- **Interactive Dashboard**: Real-time data visualization
- **Form Validation**: Client and server-side validation
- **Loading States**: User feedback during operations
- **Error Handling**: Graceful error management

## 🚀 Deployment

### Production Settings
1. Set `DEBUG = False` in settings
2. Configure production database
3. Set up static file serving
4. Configure email backend
5. Set up SSL certificates
6. Configure logging

### Recommended Hosting
- **Heroku**: Easy deployment with PostgreSQL addon
- **DigitalOcean**: VPS with Docker support
- **AWS**: EC2 with RDS PostgreSQL
- **Google Cloud**: App Engine with Cloud SQL

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Credits

- **Developed by**: IBM Team
- **Framework**: Django
- **UI Framework**: Material Design
- **AI Integration**: Google Gemini
- **Database**: PostgreSQL

## 📞 Support

For support and questions:
- Email: higherauthority@gmail.com
- Phone: +1-555-123-4567
- Office: Administration Building, Room 101

## 🔄 Version History

- **v1.0.0** - Initial release with basic complaint management
- **v1.1.0** - Added AI integration and priority assignment
- **v1.2.0** - Enhanced UI with Material Design
- **v1.3.0** - Added PDF generation and advanced analytics

---

**Note**: This project was developed for educational purposes and can be customized for different institutions and use cases.