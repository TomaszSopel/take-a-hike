-- Insert test users
INSERT INTO users (phone_number) VALUES ('1234567890');
INSERT INTO users (phone_number) VALUES ('9876543210');

-- Insert test events
INSERT INTO events (event_code, event_date, event_description, event_location)
VALUES ('cherry', '2024-08-08', 'A walk up to Cherry Hill with a picnic at the top', 'White Memorial campgrounds');

INSERT INTO events (event_code, event_date, event_description, event_location)
VALUES ('pine_mountain', '2024-09-15', 'A hike up Pine Mountain with scenic views.', 'Pine Mountain Trailhead');
