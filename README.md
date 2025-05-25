# ClientConnect - Lead Management System

**ClientConnect** is a lead management system designed for attorneys to streamline client onboarding. Built with Django REST Framework (DRF), this API allows users to create leads, list leads, view lead details, update lead statuses, and manage resumes. The project uses PostgreSQL as the database and supports Docker for easy deployment.

## Features
- **Create Leads**: Public endpoint (`POST /api/leads/`) to submit lead forms, including resume uploads.
- **Email Notifications**: Sends confirmation emails to clients and notifies admins of new leads (with attached resumes).
- **List Leads**: Authenticated users can view a list of leads (`GET /api/leads/list/`).
- **Lead Details**: Retrieve details of a specific lead (`GET /api/leads/<id>/`).
- **Update Lead Status**: Update the status of a lead (`PATCH /api/leads/<id>/update/`)—only the `state` field can be updated.
- **Resume Access**: Admins can view or download resumes via the admin panel or API (`GET /api/leads/<id>/resume/`).
- **Swagger Documentation**: API documentation available at `/swagger/`.
- **Admin Panel**: Manage leads and download resumes at `/admin/`.
- **Docker Support**: Deploy the project easily using Docker and Docker Compose.
- **Automated Tests**: Includes tests for API endpoints.

## Technologies Used
- Python 3.11
- Django 5.2.1
- Django REST Framework 3.16.0
- PostgreSQL 13
- Docker va Docker Compose
- Swagger (drf-yasg)
- Djoser
## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/OzodbekPrimov/ClientConnect.git
cd ClientConnect
