BEGIN;
CREATE TABLE IF NOT EXISTS members (
    id INTEGER,
    fn TEXT,
    ln TEXT
);
INSERT INTO members VALUES (1, "Steve", "Coplan");
INSERT INTO members VALUES (2, "Shawn", "Verzilli");
INSERT INTO members VALUES (3, "Ben", "Shew");
INSERT INTO members VALUES (4, "Robert", "Culling");
INSERT INTO members VALUES (5, "Ryan", "Bennett");
COMMIT;
