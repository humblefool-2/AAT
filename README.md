# AAT

Apps Analysis Tool (AAT) is a Python-based web application for collecting and reviewing app-related data, including application metadata, review analysis, sentiment, and code inspection artifacts. The project combines a Flask web interface with a MySQL-backed data layer and sample analysis assets.

## Overview

This repository contains a legacy Flask application and supporting analysis files. It appears to be designed for:

- user authentication and dashboard-style web pages
- storing structured data in MySQL
- analyzing app/review/code data from text-based sources
- presenting results through a lightweight browser UI

## Tech Stack

- Python
- Flask
- MySQL
- Bootstrap
- jQuery
- Werkzeug

## Repository Structure

```text
AAT/
├── app.py                  # Flask application entry point
├── a.sql                  # SQL schema/data script
├── DB_SCHEMA.txt           # Database schema documentation
├── test.py                # Additional test/analysis script
├── code.txt               # Code-related data
├── review-analysis.txt    # Review analysis output
├── sentiment.txt          # Sentiment analysis output
├── sentiments-api.txt     # Sentiment API notes/examples
├── fetch-link.txt         # Link fetching related notes
├── bs-usage.txt           # Browser/server usage notes
├── static/
│   ├── js/
│   │   ├── jquery.js
│   │   └── query.js
│   └── Uploads/           # Uploads directory
├── templates/
│   ├── index.html
│   ├── error.html
│   └── ...                # additional Flask templates
└── README.md              # Project documentation
```

## Features

- Flask-based web application with signup/signin and dashboard flows
- MySQL-backed user and wish-list style persistence
- Data analysis notes for review sentiment and app inspection
- Bootstrap-powered UI and lightweight jQuery client scripts
- Custom text-based artifacts for app analysis workflows

## Getting Started

### Prerequisites

- Python 3.8+ (project appears to be a legacy Flask app and may require compatibility adjustments)
- MySQL server running locally
- pip for installing Python packages

### Install dependencies

```bash
pip install flask flask-mysql werkzeug
```

If your environment uses newer Flask packages or a different MySQL connector, you may need to adjust imports and dependency versions for compatibility.

### Database setup

1. Create a MySQL database named `BucketList` (as configured in `app.py`)
2. Import the SQL script(s) in the repository, especially `a.sql` and the schema information in `DB_SCHEMA.txt`
3. Update the database connection settings in `app.py` if your local MySQL credentials differ

### Run the app

```bash
python app.py
```

Then open the app in your browser at:

```text
http://localhost:5000/
```

## Important Notes

This repository appears to include both:

- a web application backend for user/session flows
- supporting analysis text files used for app/review/sentiment inspection

Because the code appears to be from an older Flask/MySQL project, some modules and syntax may require modernization for current Python and Flask versions.

## Suggested Improvements

- add a `requirements.txt` file
- modernize the Flask/MySQL integration for Python 3 compatibility
- add environment variables for database credentials
- document the exact app-analysis workflow from the text assets
- provide a clean setup guide for the real data model and use cases

## License

This repository does not currently include a license file. If you intend to distribute or publish the project, add an open-source license such as MIT or Apache 2.0.

## Author / Maintainer

This project was prepared for the AAT repository and may require further cleanup and documentation based on the intended business use case.
