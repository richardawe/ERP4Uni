# ERP4Uni - University ERP System

A comprehensive Enterprise Resource Planning (ERP) system designed specifically for universities, built with Streamlit and Django.

## Features

- 📚 Library Services
  - Book catalog search
  - Borrowing management
  - Room reservations
  - Digital resources access

- 💰 Finance & Billing
  - Financial summary
  - Payment processing
  - Scholarship management
  - Financial aid applications

- 🏠 Housing Management
  - Room assignments
  - Maintenance requests
  - Housing applications
  - Facility management

## Tech Stack

- Frontend: Streamlit
- Backend: Django REST Framework (for future integration)
- Database: SQLite (development) / PostgreSQL (production)
- Authentication: Session-based with role management
- UI Components: Streamlit native components

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ERP4Uni.git
cd ERP4Uni
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Streamlit application:
```bash
streamlit run streamlit_frontend/Home.py
```

## Deployment to Netlify

1. Fork this repository to your GitHub account

2. Sign up for a Netlify account at https://www.netlify.com/

3. From the Netlify dashboard:
   - Click "New site from Git"
   - Choose GitHub as your Git provider
   - Select your forked repository
   - Configure build settings:
     - Build command: `streamlit run streamlit_frontend/Home.py`
     - Publish directory: `streamlit_frontend`

4. Environment Variables:
   Add the following environment variables in Netlify:
   ```
   PYTHON_VERSION=3.11
   STREAMLIT_SERVER_PORT=8501
   ```

5. Deploy:
   - Click "Deploy site"
   - Netlify will build and deploy your application

## Project Structure

```
ERP4Uni/
├── streamlit_frontend/     # Streamlit application
│   ├── Home.py            # Main application entry
│   ├── pages/             # Application pages
│   ├── utils/             # Utility functions
│   └── config.py          # Configuration settings
├── requirements.txt       # Python dependencies
├── netlify.toml          # Netlify configuration
├── runtime.txt           # Python version specification
└── README.md            # Project documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the development team. 