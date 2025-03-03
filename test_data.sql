--
-- PostgreSQL database dump
--

-- Dumped from database version 12.20 (Ubuntu 12.20-1.pgdg22.04+1)
-- Dumped by pg_dump version 12.20 (Ubuntu 12.20-1.pgdg22.04+1)

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

--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: gitpod
--



--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: gitpod
--

INSERT INTO public.users (user_id, phone_number, is_admin) VALUES (1, '8883331234', false);


--
-- Data for Name: user_event_signups; Type: TABLE DATA; Schema: public; Owner: gitpod
--



--
-- Name: events_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gitpod
--

SELECT pg_catalog.setval('public.events_event_id_seq', 1, false);


--
-- Name: user_event_signups_user_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gitpod
--

SELECT pg_catalog.setval('public.user_event_signups_user_event_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gitpod
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, true);


--
-- PostgreSQL database dump complete
--

