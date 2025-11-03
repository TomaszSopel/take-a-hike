# Take a Hike SMS Alert System

## Overview

This project aims to address the issue of no-shows for scheduled hikes at local conservation centers. It provides an SMS alert system to remind participants about upcoming hikes and allows administrators to see who's signed up for alerts.

## Features

*   **SMS Alerts:** Sends automated SMS reminders to participants who sign up for hikes.
*   **Administrator Interface:** Allows administrators to view sign-up lists.

## Technologies Used

*   **Twilio API:** Used for sending and receiving SMS messages.
*   **PostgreSQL:** Used for storing participant data and hike schedules.
*   **Docker:** Used for containerization.
*   **Heroku CLI:** Used for deployment.
*   **Python:** Used for backend logic.

## Setup

1.  Clone the repository.
2.  Install the required dependencies using `pip install -r requirements.txt`.
3.  Set up a PostgreSQL database. The database name should be `take_a_hike`.
4.  Run the `schema.sql` file to create the necessary tables.
5.  Set your Twilio API credentials as environment variables (TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER).
6.  Run the application using `python main.py`.

## Usage

1.  Participants sign up for a hike through the conservation center.
2.  The system automatically adds the participant's phone number to the alert list for the specific hike.
3.  Administrators can view the list of participants signed up for alerts.

## Future Development

*   Add support for different types of alerts (e.g., weather updates).
*   Integrate with existing registration systems.
*   Implement automated roll call functionality the day before a scheduled hike.
