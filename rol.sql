--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.3

-- Started on 2023-07-26 16:00:42

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
-- TOC entry 273 (class 1259 OID 25704)
-- Name: sec_rol; Type: TABLE; Schema: public; Owner: osbustaman
--

CREATE TABLE public.sec_rol (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    rol_id integer NOT NULL,
    rol_name character varying(70) NOT NULL,
    rol_active character varying(1) NOT NULL,
    rol_client character varying(1) NOT NULL,
    rol_nivel integer NOT NULL
);


ALTER TABLE public.sec_rol OWNER TO osbustaman;

--
-- TOC entry 272 (class 1259 OID 25703)
-- Name: sec_rol_rol_id_seq; Type: SEQUENCE; Schema: public; Owner: osbustaman
--

CREATE SEQUENCE public.sec_rol_rol_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sec_rol_rol_id_seq OWNER TO osbustaman;

--
-- TOC entry 3479 (class 0 OID 0)
-- Dependencies: 272
-- Name: sec_rol_rol_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osbustaman
--

ALTER SEQUENCE public.sec_rol_rol_id_seq OWNED BY public.sec_rol.rol_id;


--
-- TOC entry 3327 (class 2604 OID 25707)
-- Name: sec_rol rol_id; Type: DEFAULT; Schema: public; Owner: osbustaman
--

ALTER TABLE ONLY public.sec_rol ALTER COLUMN rol_id SET DEFAULT nextval('public.sec_rol_rol_id_seq'::regclass);


--
-- TOC entry 3473 (class 0 OID 25704)
-- Dependencies: 273
-- Data for Name: sec_rol; Type: TABLE DATA; Schema: public; Owner: osbustaman
--

COPY public.sec_rol (created, modified, rol_id, rol_name, rol_active, rol_client, rol_nivel) FROM stdin;
2023-07-26 14:47:46.837233-04	2023-07-26 15:22:06.83937-04	1	colaborador	S	S	1
2023-07-26 14:48:14.406231-04	2023-07-26 15:22:14.049371-04	2	lider-equipo	S	S	2
2023-07-26 14:48:30.708271-04	2023-07-26 15:22:21.178376-04	3	recursos humanos	S	S	3
2023-07-26 15:03:26.765077-04	2023-07-26 15:22:31.030372-04	4	lokilabs	S	N	8
\.


--
-- TOC entry 3480 (class 0 OID 0)
-- Dependencies: 272
-- Name: sec_rol_rol_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osbustaman
--

SELECT pg_catalog.setval('public.sec_rol_rol_id_seq', 4, true);


--
-- TOC entry 3329 (class 2606 OID 25709)
-- Name: sec_rol sec_rol_pkey; Type: CONSTRAINT; Schema: public; Owner: osbustaman
--

ALTER TABLE ONLY public.sec_rol
    ADD CONSTRAINT sec_rol_pkey PRIMARY KEY (rol_id);


-- Completed on 2023-07-26 16:00:42

--
-- PostgreSQL database dump complete
--

