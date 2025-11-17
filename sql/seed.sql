SET ECHO ON VERIFY OFF FEEDBACK ON

PROMPT === POPULATING TABLES ===
PROMPT === MOVIES POPULATED ===

INSERT INTO Movies (ID, Movie_Name, Price, Genre, Copies, Avg_Rating, Release_Date, Runtime_Min, Age_Rating, Language_Code) VALUES
('M001','Avengers: Assemble', 3.99, 'Action', 4, 4.3, DATE '2012-05-01', 143, 'PG-13', 'EN');
INSERT INTO Movies VALUES
('M002','Spirited Away',        2.99,'Fantasy', 3, 3.0, DATE '2001-07-20', 125, 'PG',   'JP');
INSERT INTO Movies VALUES
('M003','Parasite',             4.49,'Thriller',3, 2.1, DATE '2019-05-30', 132, 'R',    'KO');
INSERT INTO Movies VALUES
('M004','3 Idiots',             2.49,'Comedy',  2, 4.4, DATE '2009-12-25', 170, 'PG',   'HI');
INSERT INTO Movies VALUES
('M005','The Dark Knight',      3.99,'Action',  4, 5.0, DATE '2008-07-18', 152, 'PG-13','EN');
INSERT INTO Movies VALUES
('M006','Saiyaara',      13.99,'Romance',  2, 3.0, DATE '2025-04-23', 180, 'PG-13','EN');

PROMPT === CUSTOMERS POPULATED ===
INSERT INTO Customer (Username,Balance,Password,First_Name,Last_Name,Age,Email,Phone) VALUES
('alice',  10.00,'passAlice','Alice','Nguyen',   22,'alice@gmail.com','+1-416-555-1001');
INSERT INTO Customer VALUES
('bob',     5.50,'passBob',  'Bob',  'Singh',    25,'bob@gmail.com',  '+1-416-555-1002');
INSERT INTO Customer VALUES
('carol',  20.00,'passCarol','Carol','Perez',    31,'carol@gmail.com','+1-416-555-1003');
INSERT INTO Customer VALUES
('dave',    0.00,'passDave', 'Dave', 'Kim',      19,'dave@gmail.com', '+1-416-555-1004');
INSERT INTO Customer VALUES
('eve',    14.25,'passEve',  'Eve',  'Rahman',   27,'eve@gmail.com',  '+1-416-555-1005');


PROMPT == INVENTORY POPULATED ===
INSERT INTO Inventory (Copy_ID, Movie_ID, Quality, Status) VALUES ('AVG01', 'M001','4K','AVAILABLE');  
INSERT INTO Inventory (Copy_ID, Movie_ID, Quality, Status) VALUES ('AVG02', 'M001','1080P','RENTED');  
INSERT INTO Inventory (Copy_ID, Movie_ID, Quality, Status) VALUES ('AVG03', 'M001','1080P','AVAILABLE');
INSERT INTO Inventory (Copy_ID, Movie_ID, Quality, Status) VALUES ('AVG04', 'M001','720P','RESERVED'); 


INSERT INTO Inventory (Copy_ID, Movie_ID, Quality, Status) VALUES ('SPI05', 'M002','1080P','AVAILABLE');
INSERT INTO Inventory (Copy_ID, Movie_ID, Quality, Status) VALUES ('SPI06', 'M002','4K','RENTED');
INSERT INTO Inventory (Copy_ID, Movie_ID, Quality, Status) VALUES ('SPI07', 'M002','480P','AVAILABLE');


INSERT INTO Inventory (Copy_ID, Movie_ID, Quality, Status) VALUES ('PARA08', 'M003','1080P','AVAILABLE');
INSERT INTO Inventory (Copy_ID, Movie_ID, Quality, Status) VALUES ('PARA09', 'M003','1080P','RENTED');
INSERT INTO Inventory (Copy_ID, Movie_ID, Quality, Status) VALUES ('PARA10', 'M003','720P','AVAILABLE');


INSERT INTO Inventory (Copy_ID, Movie_ID, Quality, Status) VALUES ('IDI1', 'M004','1080P','AVAILABLE');
INSERT INTO Inventory (Copy_ID, Movie_ID, Quality, Status) VALUES ('IDI2', 'M004','720P','AVAILABLE');

INSERT INTO Inventory (Copy_ID, Movie_ID, Quality, Status) VALUES ('DARK1', 'M005','4K','AVAILABLE');
INSERT INTO Inventory (Copy_ID, Movie_ID, Quality, Status) VALUES ('DARK2', 'M005','1080P','RENTED');
INSERT INTO Inventory (Copy_ID, Movie_ID, Quality, Status) VALUES ('DARK3', 'M005','1080P','AVAILABLE');
INSERT INTO Inventory (Copy_ID, Movie_ID, Quality, Status) VALUES ('DARK4', 'M005','480P','AVAILABLE');

INSERT INTO Inventory (Copy_ID, Movie_ID, Quality, Status) VALUES ('SAIY1', 'M006','1080P','AVAILABLE');
INSERT INTO Inventory (Copy_ID, Movie_ID, Quality, Status) VALUES ('SAIY2', 'M006','720P','AVAILABLE');

PROMPT === LIBRARY POPULATED ===
-- Bob is renting Avengers copy AVG02 starting 2025-09-24 (due 2025-10-01)
INSERT INTO Library (Username, Movie_ID, Copy_ID, Start_Date, Returned_On)
VALUES ('bob','M001','AVG02', DATE '2025-09-24', NULL);

-- Alice rented Spirited Away copy SPI06 from 2025-09-10 and returned 2025-09-12
INSERT INTO Library (Username, Movie_ID, Copy_ID, Start_Date, Returned_On)
VALUES ('alice','M002','SPI06', DATE '2025-09-10', DATE '2025-09-12');

-- Dave rented Parasite copy PARA09 on 2025-09-15 (due 2025-09-22), not returned
INSERT INTO Library (Username, Movie_ID, Copy_ID, Start_Date, Returned_On)
VALUES ('dave','M003','PARA09', DATE '2025-09-15', NULL);

-- Eve rented The Dark Knight copy DARK2 on 2025-09-26 (due 2025-10-03), active
INSERT INTO Library (Username, Movie_ID, Copy_ID, Start_Date, Returned_On)
VALUES ('eve','M005','DARK2', DATE '2025-09-26', NULL);

-- Carol rented 3 Idiots copy IDI1 on 2025-09-18 and returned 2025-09-20
INSERT INTO Library (Username, Movie_ID, Copy_ID, Start_Date, Returned_On)
VALUES ('carol','M004','IDI1', DATE '2025-09-18', DATE '2025-09-20');

-- Alice rented Avengers copy AVG03 on 2025-09-01 and returned 2025-09-04
INSERT INTO Library (Username, Movie_ID, Copy_ID, Start_Date, Returned_On)
VALUES ('alice','M001','AVG03', DATE '2025-09-01', DATE '2025-09-04');

PROMPT === POPULATED CONTENT MANAGER ===
INSERT INTO CONTENT_MANAGER(EMPLOYEE_ID, Password, MOVIE_TO_CHANGE, EMAIL) VALUES
('51090', 'charlie123', 'Parasite', 'charlie@gmail.com');
INSERT INTO CONTENT_MANAGER(EMPLOYEE_ID, Password, MOVIE_TO_CHANGE, EMAIL) VALUES
('52091', 'diana456', 'Titanic', 'diana@gmail.com');
INSERT INTO CONTENT_MANAGER(EMPLOYEE_ID, Password, MOVIE_TO_CHANGE, EMAIL) VALUES
('53092', 'edward789', 'Inception', 'edward@gmail.com');

PROMPT === POPULATED CUSTOMER SERVICE ===
INSERT INTO CUSTOMER_SERVICE(EMPLOYEE_ID, Password, SHIFT, EMAIL) VALUES
('60001', 'Josh123', 'Morning', 'Josh@gmail.com');
INSERT INTO CUSTOMER_SERVICE(EMPLOYEE_ID, Password, SHIFT, EMAIL) VALUES
('60002', 'Zach223', 'Afternoon', 'Zach@gmail.com');
INSERT INTO CUSTOMER_SERVICE(EMPLOYEE_ID, Password, SHIFT, EMAIL) VALUES
('60003', 'Pokemon223', 'Night', 'Pokemon@gmail.com');

PROMPT === POPULATED DEVELOPER ===
INSERT INTO DEVELOPER(EMPLOYEE_ID, Password, SPECIALTY, EMAIL, GITHUB) VALUES
('70001', 'Python123', 'BACKEND', 'Jelly@gmail.com', 'https://github.com/zach1');
INSERT INTO DEVELOPER(EMPLOYEE_ID, Password, SPECIALTY, EMAIL, GITHUB) VALUES
('70002', 'HTML123', 'FRONTEND', 'Jaiden@gmail.com', 'https://github.com/Jaiden2');

PROMPT === POPULATED REVIEWS ===
INSERT INTO Review (Username, Movie_ID, Rating, Review_text, Created_At, REVIEW_ID) VALUES
('alice', 'M001', 4, 'Amazing movie with great action scenes!', DATE '2025-09-05', 1132);
INSERT INTO Review (Username, Movie_ID, Rating, Review_text, Created_At, REVIEW_ID) VALUES
('bob', 'M002', 5, 'A beautiful and enchanting film.', DATE '2025-09-15', 2214);

COMMIT;
EXIT;