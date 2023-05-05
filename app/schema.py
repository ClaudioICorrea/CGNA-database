instructions = [
    "SET FOREIGN_KEY_CHECKS=0;",
    "DROP TABLE IF EXISTS user;",
    "DROP TABLE IF EXISTS queries;",
    "DROP TABLE IF EXISTS species;",
    "DROP TABLE IF EXISTS chromosomes;",
    "DROP TABLE IF EXISTS genes;",
    "SET FOREIGN_KEY_CHECKS=1;",
    """
           CREATE TABLE user (
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(1000) NOT NULL
        )
    """,
    """
        CREATE TABLE queries (
            id INT PRIMARY KEY AUTO_INCREMENT,
            created_by INT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            id_specie INT,
            id_chromosome INT,
            id_genes INT,
            name_gen VARCHAR(255),
            FOREIGN KEY (created_by) REFERENCES user (id)
        )
    """,
    """
        CREATE TABLE species (
            id_specie INT PRIMARY KEY AUTO_INCREMENT,
            specie VARCHAR(255) UNIQUE NOT NULL
        )
    """,
    """
        CREATE TABLE chromosomes(
            id_chromosome VARCHAR(255) PRIMARY KEY NOT NULL,
            id_specie INT NOT NULL,
            gbig VARCHAR(255),
            number_genes INT(11),   
            size INT(11),
            alias VARCHAR(255), 
            sequence LONGTEXT,
            FOREIGN KEY fk_id_specie(id_specie) REFERENCES species(id_specie)
        )
    """,
    """
        CREATE TABLE genes (
            id_genes VARCHAR(255) PRIMARY KEY NOT NULL,
            id_chromosome VARCHAR(255) NOT NULL,
            bio_type VARCHAR(255),
            start INT(11) NOT NULL,
            end INT(11) NOT NULL,
            score  VARCHAR(255),
            strand VARCHAR(255),
            frame VARCHAR(255),
            size INT(11),
            name_gen VARCHAR(255),
            FOREIGN KEY fk_id_chromosome(id_chromosome) REFERENCES chromosomes(id_chromosome)
        );
    """,
    "INSERT INTO species (specie) VALUES ('Arabidopsis_thaliana');",
]