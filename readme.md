# Snapscale Intranet
## Overview
**Snapscale Intranet** is a Django-based web application developed and maintained by SNAPSCALE to support internal operations.

This project is intended for internal use only and is not publicly available or distributed.

## Features
- Secure login and role-based access control
- Integrated with LDAP for user authentication
- Modular admin interface for managing data
- Integration with internal APIs and third-party services

## Tech Stack
- Python 3.10
- Django 4.x
- PostgreSQL
- Bootstrap 5
- Apache For virtual host and redirection
- Let's Encrypt for SSL certificate

## Getting Started

### Local Development Setup
- Server Ubuntu 24.04
  -  Local Ip Address: 10.10.10.14
  - Apache Virtual Host
    - /etc/apache2/sites-available/crm-snapscaleapps-com.conf
    - /etc/apache2/sites-enabled/crm-snapscaleapps-com-le-ssl.conf
  - Python 3.12
    - Virtual Environment
      - /opt/crm-intranet-env
    - Django Project (Snapscale Intranet Root Directory)    
      - /opt/crm-intranet-web/
        - .env - Environment Variables
        - requirements.txt - Python Package Dependencies
  - Custom Django Service File
    - /etc/systemd/system/django-crm-intranet.service

## Contributing
This is an internal project maintained by the Workplace Tech Team at Snapscale.

## License
This project is proprietary and confidential.
All rights reserved © Snapscale, 2025.

