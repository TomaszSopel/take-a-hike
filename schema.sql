CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    phone_number VARCHAR(15) UNIQUE NOT NULL
);

CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    event_code VARCHAR(50) UNIQUE NOT NULL,
    event_name VARCHAR(100) NOT NULL,
    event_date DATE NOT NULL,
    event_description TEXT,
    event_location VARCHAR(100)
);

CREATE TABLE user_event_signups (
    user_event_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    event_id INTEGER REFERENCES events(event_id),
    signup_date DATE NOT NULL,
    attendance_confirmed BOOLEAN DEFAULT FALSE
);