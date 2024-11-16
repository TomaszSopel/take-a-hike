--
-- PostgreSQL database dump
--

-- Dumped from database version 12.19 (Ubuntu 12.19-1.pgdg22.04+1)
-- Dumped by pg_dump version 12.19 (Ubuntu 12.19-1.pgdg22.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: events; Type: TABLE; Schema: public; Owner: gitpod
--

CREATE TABLE public.events (
    event_id integer NOT NULL,
    event_code character varying(50) NOT NULL,
    event_date date,
    event_description text,
    event_location character varying(150),
    event_name character varying(100)
);


ALTER TABLE public.events OWNER TO gitpod;

--
-- Name: events_event_id_seq; Type: SEQUENCE; Schema: public; Owner: gitpod
--

CREATE SEQUENCE public.events_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_event_id_seq OWNER TO gitpod;

--
-- Name: events_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gitpod
--

ALTER SEQUENCE public.events_event_id_seq OWNED BY public.events.event_id;


--
-- Name: user_event_signups; Type: TABLE; Schema: public; Owner: gitpod
--

CREATE TABLE public.user_event_signups (
    user_event_id integer NOT NULL,
    user_id integer,
    event_id integer,
    signup_date date DEFAULT CURRENT_DATE,
    attendance_confirmed boolean DEFAULT false
);


ALTER TABLE public.user_event_signups OWNER TO gitpod;

--
-- Name: user_event_signups_user_event_id_seq; Type: SEQUENCE; Schema: public; Owner: gitpod
--

CREATE SEQUENCE public.user_event_signups_user_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_event_signups_user_event_id_seq OWNER TO gitpod;

--
-- Name: user_event_signups_user_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gitpod
--

ALTER SEQUENCE public.user_event_signups_user_event_id_seq OWNED BY public.user_event_signups.user_event_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: gitpod
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    phone_number character varying(15) NOT NULL
);


ALTER TABLE public.users OWNER TO gitpod;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: gitpod
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO gitpod;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gitpod
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: events event_id; Type: DEFAULT; Schema: public; Owner: gitpod
--

ALTER TABLE ONLY public.events ALTER COLUMN event_id SET DEFAULT nextval('public.events_event_id_seq'::regclass);


--
-- Name: user_event_signups user_event_id; Type: DEFAULT; Schema: public; Owner: gitpod
--

ALTER TABLE ONLY public.user_event_signups ALTER COLUMN user_event_id SET DEFAULT nextval('public.user_event_signups_user_event_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: gitpod
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: gitpod
--

COPY public.events (event_id, event_code, event_date, event_description, event_location, event_name) FROM stdin;
1	cherry	2024-08-08	A walk up to Cherry Hill with a picnic at the top	White Memorial campgrounds	\N
2	pine_mountain	2024-09-15	A hike up Pine Mountain with scenic views.	Pine Mountain Trailhead	\N
\.


--
-- Data for Name: user_event_signups; Type: TABLE DATA; Schema: public; Owner: gitpod
--

COPY public.user_event_signups (user_event_id, user_id, event_id, signup_date, attendance_confirmed) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: gitpod
--

COPY public.users (user_id, phone_number) FROM stdin;
3	2345678901
4	1234567890
5	9876543210
\.


--
-- Name: events_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gitpod
--

SELECT pg_catalog.setval('public.events_event_id_seq', 2, true);


--
-- Name: user_event_signups_user_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gitpod
--

SELECT pg_catalog.setval('public.user_event_signups_user_event_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gitpod
--

SELECT pg_catalog.setval('public.users_user_id_seq', 5, true);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: gitpod
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (event_id);


--
-- Name: user_event_signups user_event_signups_pkey; Type: CONSTRAINT; Schema: public; Owner: gitpod
--

ALTER TABLE ONLY public.user_event_signups
    ADD CONSTRAINT user_event_signups_pkey PRIMARY KEY (user_event_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: gitpod
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: user_event_signups user_event_signups_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gitpod
--

ALTER TABLE ONLY public.user_event_signups
    ADD CONSTRAINT user_event_signups_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(event_id);


--
-- Name: user_event_signups user_event_signups_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gitpod
--

ALTER TABLE ONLY public.user_event_signups
    ADD CONSTRAINT user_event_signups_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

