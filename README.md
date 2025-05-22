# ClientConnect - Lead Management API

This project is a lead management system designed for attorneys. Built with Django REST Framework (DRF), the API allows creating leads, listing leads, retrieving individual lead details, and updating lead status. It uses PostgreSQL as the database and supports Docker for easy deployment.

## Features
- **Create a New Lead**: Public endpoint (`POST /api/leads/`) to submit lead forms and confirm submission.
- **Email Notifications**: Sends a confirmation email to the client and a notification to the admin upon form submission.
- **List Leads**: Retrieve a list of leads for authenticated users (`GET /api/leads/`).
- **Lead Details**: View details of a specific lead (`GET /api/leads/<id>/`).
- **Update Lead Status**: Update the status of a lead (`PATCH /api/leads/<id>/`).
- **Swagger Documentation**: API documentation available via Swagger (`/swagger/`).
- **Admin Panel**: Manage leads through Django's admin panel (`/admin/`).
- **Docker Support**: Easily deploy the project using Docker and Docker Compose.
- **Tests**: Automated tests for API endpoints.

## Technologies
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
