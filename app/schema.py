instructions = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS flat;',
    'SET FOREIGN_KEY_CHECKS=1;',
    """
        CREATE TABLE flat (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50) UNIQUE NOT NULL,
            description VARCHAR(100) NOT NULL,
            sequence VARCHAR(100) NOT NULL
        )
    """
]