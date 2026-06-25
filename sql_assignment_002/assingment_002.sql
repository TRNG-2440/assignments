CREATE SCHEMA assignment02;

CREATE TABLE assignment02.principles(
		principle_id INTEGER PRIMARY KEY,
		first_name VARCHAR(200),
		last_name VARCHAR(200),
		hire_date VARCHAR(200),
		salary INTEGER
);

CREATE TABLE assignment02.schools(
		school_id INTEGER PRIMARY KEY,
		principle_id INTEGER,
		
		CONSTRAINT principle_id_fk FOREIGN KEY (principle_id) REFERENCES assignment02.principles(principle_id)
);

CREATE TABLE assignment02.students(
		student_id INTEGER PRIMARY KEY,
		school_id INTEGER,
		principle_id INTEGER,
		first_name VARCHAR(200),
		last_name VARCHAR(200),
		grade INTEGER,
		address VARCHAR(200),
		emergency_contact VARCHAR(200),

		CONSTRAINT school_id_fk FOREIGN KEY (school_id) REFERENCES assignment02.schools(school_id),
		CONSTRAINT principle_id_fk FOREIGN KEY (principle_id) REFERENCES assignment02.principles(principle_id)
		
);