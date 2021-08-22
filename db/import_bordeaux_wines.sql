CREATE TABLE attributes (
    id          INT PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    aoc         VARCHAR(255) NOT NULL,
    cuvee       VARCHAR(255),
    price       NUMERIC(8,3),
    quantity    FLOAT,
    wine        VARCHAR(255) NOT NULL,
    year        INT,
    score       INT,
    tastes      JSON NOT NULL
);

COPY attributes(id, name, aoc, cuvee, price, quantity, wine, year, score, tastes)
FROM '/docker-entrypoint-initdb.d/bordeaux_wines_bdd_ready.csv'
DELIMITER ';'
CSV HEADER;

SELECT
    id,
    wine AS name,
    year AS millesime
INTO
    wines
FROM
    attributes;

CREATE INDEX ON wines (name);
CREATE INDEX ON wines (millesime);

ALTER TABLE
    wines
ADD PRIMARY KEY (id),
ADD CONSTRAINT wines_attributes_fk FOREIGN KEY (id) REFERENCES attributes (id);

ALTER TABLE
    attributes
DROP COLUMN name,
DROP COLUMN aoc,
DROP COLUMN cuvee,
DROP COLUMN price,
DROP COLUMN quantity,
DROP COLUMN wine,
DROP COLUMN year,
DROP COLUMN score;



-- FINAL TABLES
--
-- CREATE TABLE attributes (
--     id          INT PRIMARY KEY,
--     tastes      JSON NOT NULL,
-- );
--
--
-- CREATE TABLE wines (
--     id          INT PRIMARY KEY,
--     name        VARCHAR(255) NOT NULL,
--     millesime  INT,

--     FOREIGN KEY (id)
--         REFERENCES attributes (id)
-- );