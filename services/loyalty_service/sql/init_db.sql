--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0
-- Dumped by pg_dump version 16.0

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
-- Name: loyalty; Type: TABLE; Schema: public; Owner: program
--

CREATE TABLE public.loyalty (
    id integer NOT NULL,
	username varchar(80) NOT NULL,
	reservation_count integer NOT NULL,
	status varchar(80) NOT NULL CHECK (status IN ('BRONZE', 'SILVER', 'GOLD')),
	discount integer NOT NULL
);


ALTER TABLE public.loyalty OWNER TO program;

--
-- Name: loyalty_id_seq; Type: SEQUENCE; Schema: public; Owner: program
--

CREATE SEQUENCE public.loyalty_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.loyalty_id_seq OWNER TO program;

--
-- Name: ticket_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: program
--

ALTER SEQUENCE public.loyalty_id_seq OWNED BY public.loyalty.id;


--
-- Name: ticket id; Type: DEFAULT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.loyalty ALTER COLUMN id SET DEFAULT nextval('public.loyalty_id_seq'::regclass);


--
-- Data for Name: loyalty; Type: TABLE DATA; Schema: public; Owner: program
--

COPY public.loyalty (id, username, reservation_count, status, discount) FROM stdin;
1	Test Max	25	GOLD	10
\.


--
-- Name: loyalty_id_seq; Type: SEQUENCE SET; Schema: public; Owner: program
--

SELECT pg_catalog.setval('public.loyalty_id_seq', 1, false);


--
-- Name: loyalty loyalty_pkey; Type: CONSTRAINT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.loyalty
    ADD CONSTRAINT loyalty_pkey PRIMARY KEY (id);

--
-- PostgreSQL database dump complete
--