# Gemini Project Configuration

This file helps the Gemini assistant understand the project's structure, technologies, and conventions.

## Project Overview

This is a monorepo project with a Nuxt.js frontend and a Django backend.

## Frontend (`apps/client`)

*   **Framework:** Nuxt.js 3
*   **State Management:** Pinia
*   **Data Fetching:** Vue Query
*   **UI:** Lucide Icons, and likely a custom component library.
*   **Styling:** Sass, Stylelint, Prettier
*   **Testing:** Lighthouse CI

## Backend (`apps/server`)

*   **Framework:** Django
*   **API:** Django REST Framework
*   **Async Tasks:** Celery
*   **Database:** PostgreSQL (based on psycopg2)
*   **Authentication:** djangorestframework-simplejwt
*   **Testing:** Pytest, Flake8, Pylint

## Future Tasks

*   ulb_tips
