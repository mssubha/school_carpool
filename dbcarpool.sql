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
1	1	HONDA	Accord	4HHU765	f	f	3
2	2	SUBARU	Ascent	8JJC654	t	t	4
3	3	TOYOTA	Prius	8BBF543	t	f	2
4	4	TESLA	Model 3	9HHS543	f	t	2
5	5	TOYOTA	Prius	2MAY654	f	f	2
6	6	TESLA	Model 3	9AWP765	t	t	2
7	7	HONDA	Odyssey	1NAD875	t	f	5
8	8	HONDA	Odyssey	4SSN729	f	t	4
\.


--
-- Data for Name: children; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.children (child_id, user_id, name, grade) FROM stdin;
1	1	Angele	3
2	2	Briana	4
3	3	Cathy	4
4	4	Ashley	5
5	5	Noah	2
6	6	Mark	4
7	7	Micha	3
8	8	Mathew	5
9	2	Sweets	4
10	4	Audrey	1
11	5	Diana	2
12	7	Noah	3
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
1	tester13132@test.com	tester1	Steve	Brenda	415-234-4564	24 Galerita Way	San Rafael	CA	94903	38.013545299999997	-122.516402099999993	01010000007CC564BB0CA15EC0DB4136DABB014340
2	2tester2@test.com	tester2	Alex	Maggie	415-345-3345	17 Adrian Terrace	San Rafael	CA	94903	38.0124429999999975	-122.515548999999993	0101000000129F3BC1FEA05EC0350873BB97014340
3	3tester3@test.com	tester3	Jennifer	Bruce	415-345-4564	21 Olive Ct	Novato	CA	94945	38.1063745000000083	-122.550479499999994	010100000094675E0E3BA35EC06F50FBAD9D0D4340
4	4tester4@test.com	tester4	Sarah	Collet	650-235-3555	3 Adrian Way	San Rafael	CA	94903	38.0078833000000031	-122.522401500000001	01010000006878B3066FA15EC0A0D7E95102014340
5	5tester5@test.com	tester5	Jenny	Adrienne	408-245-6565	3 Randolph Dr	 Novato	CA	94949	38.0546840000000017	-122.525458299999997	01010000005A7AD91BA1A15EC0A7CEA3E2FF064340
6	6tester6@test.com	tester6	Subha	Krishna	415-245-5645	5 Washington Avenue	San Rafael	CA	94903	37.9987798000000083	-122.526437999999999	0101000000C9570229B1A15EC0E6733804D8FF4240
7	7tester7@test.com	tester7	Stephie	Alex	415-355-5355	33 Adrian Way	San Rafael	CA	94903	38.0096150999999978	-122.5213581	01010000004D405DEE5DA15EC01D064E113B014340
8	8tester8@test.com	tester8	Maddy	Briana	415-344-5535	25 Vendola Dr	San Rafael	CA	94903	38.0097260000000006	-122.522550600000002	01010000005560127871A15EC0E0F599B33E014340
\.


--
-- Name: cars_car_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.cars_car_id_seq', 8, true);


--
-- Name: children_child_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.children_child_id_seq', 12, true);


--
-- Name: requests_request_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.requests_request_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.users_user_id_seq', 8, true);


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

