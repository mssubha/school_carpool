--
-- PostgreSQL database dump
--

-- Dumped from database version 10.14 (Ubuntu 10.14-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.14 (Ubuntu 10.14-0ubuntu0.18.04.1)

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
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: cars; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.cars (
    car_id integer NOT NULL,
    user_id integer,
    car_make character varying,
    car_model character varying,
    license_plate character varying NOT NULL,
    smoking boolean,
    pets boolean,
    seats integer NOT NULL
);


ALTER TABLE public.cars OWNER TO vagrant;

--
-- Name: cars_car_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.cars_car_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cars_car_id_seq OWNER TO vagrant;

--
-- Name: cars_car_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.cars_car_id_seq OWNED BY public.cars.car_id;


--
-- Name: children; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.children (
    child_id integer NOT NULL,
    user_id integer,
    name character varying,
    grade integer
);


ALTER TABLE public.children OWNER TO vagrant;

--
-- Name: children_child_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.children_child_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.children_child_id_seq OWNER TO vagrant;

--
-- Name: children_child_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.children_child_id_seq OWNED BY public.children.child_id;


--
-- Name: requests; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.requests (
    request_id integer NOT NULL,
    from_user integer,
    to_user integer,
    child_id integer,
    request_note text,
    decision_note text,
    request_status character varying,
    request_datetime timestamp without time zone,
    response_dateime timestamp without time zone
);


ALTER TABLE public.requests OWNER TO vagrant;

--
-- Name: requests_request_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.requests_request_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.requests_request_id_seq OWNER TO vagrant;

--
-- Name: requests_request_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.requests_request_id_seq OWNED BY public.requests.request_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    household1 character varying NOT NULL,
    household2 character varying,
    phone_number character varying NOT NULL,
    address_street character varying NOT NULL,
    address_city character varying NOT NULL,
    address_state character varying NOT NULL,
    address_zip character varying NOT NULL,
    address_latitude double precision,
    address_longitude double precision,
    address_geo public.geometry(Point)
);


ALTER TABLE public.users OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: cars car_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.cars ALTER COLUMN car_id SET DEFAULT nextval('public.cars_car_id_seq'::regclass);


--
-- Name: children child_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.children ALTER COLUMN child_id SET DEFAULT nextval('public.children_child_id_seq'::regclass);


--
-- Name: requests request_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.requests ALTER COLUMN request_id SET DEFAULT nextval('public.requests_request_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: cars; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.cars (car_id, user_id, car_make, car_model, license_plate, smoking, pets, seats) FROM stdin;
1	1	Subaru	Ascent	2JJK738	f	f	4
2	2	Toyota	Prius	4HHU734	f	t	3
\.


--
-- Data for Name: children; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.children (child_id, user_id, name, grade) FROM stdin;
\.


--
-- Data for Name: requests; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.requests (request_id, from_user, to_user, child_id, request_note, decision_note, request_status, request_datetime, response_dateime) FROM stdin;
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.users (user_id, email, password, household1, household2, phone_number, address_street, address_city, address_state, address_zip, address_latitude, address_longitude, address_geo) FROM stdin;
1	user1@test.com	123	User1	User2	415-340-4344	3 Adrian Way	San rafael	CA	94903	0	0	\N
2	user3@test.com	123	User3	User2	415-340-2334	3 Adrian Way	San Francisco	CA	94903	0	0	\N
3	user15@test.com	help	Usertets	User2	415-340-4224	21 Labrea	Foster City	CA	94253	0	0	\N
\.


--
-- Name: cars_car_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.cars_car_id_seq', 2, true);


--
-- Name: children_child_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.children_child_id_seq', 1, false);


--
-- Name: requests_request_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.requests_request_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.users_user_id_seq', 3, true);


--
-- Name: cars cars_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.cars
    ADD CONSTRAINT cars_pkey PRIMARY KEY (car_id);


--
-- Name: children children_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.children
    ADD CONSTRAINT children_pkey PRIMARY KEY (child_id);


--
-- Name: requests requests_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_pkey PRIMARY KEY (request_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: idx_users_address_geo; Type: INDEX; Schema: public; Owner: vagrant
--

CREATE INDEX idx_users_address_geo ON public.users USING gist (address_geo);


--
-- Name: cars cars_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.cars
    ADD CONSTRAINT cars_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: children children_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.children
    ADD CONSTRAINT children_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: requests requests_child_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_child_id_fkey FOREIGN KEY (child_id) REFERENCES public.children(child_id);


--
-- Name: requests requests_from_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_from_user_fkey FOREIGN KEY (from_user) REFERENCES public.users(user_id);


--
-- Name: requests requests_to_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_to_user_fkey FOREIGN KEY (to_user) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

