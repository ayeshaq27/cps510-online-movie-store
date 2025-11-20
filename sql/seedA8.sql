SET ECHO ON VERIFY OFF FEEDBACK ON

PROMPT === POPULATING TABLES ===

------------------------------------------------------------
-- MOVIE_INFORMATION
------------------------------------------------------------
PROMPT === MOVIE_INFORMATION POPULATED ===

INSERT INTO Movie_information
(Movie_ID, Movie_Name, Price, Genre, Copies, Avg_Rating, Release_Date, Runtime_Min, Age_Rating, Language_Code)
VALUES
('M001','Avengers: Assemble', 3.99,'Action', 4, 4.3, DATE '2012-05-01',143,'PG-13','EN');
INSERT INTO Movie_information VALUES
('M002','Spirited Away',        2.99,'Fantasy', 3, 3.0, DATE '2001-07-20',125,'PG',   'JP');
INSERT INTO Movie_information VALUES
('M003','Parasite',             4.49,'Thriller',3, 2.1, DATE '2019-05-30',132,'R',    'KO');
INSERT INTO Movie_information VALUES
('M004','3 Idiots',             2.49,'Comedy',  2, 4.4, DATE '2009-12-25',170,'PG',   'HI');
INSERT INTO Movie_information VALUES
('M005','The Dark Knight',      3.99,'Action',  4, 5.0, DATE '2008-07-18',152,'PG-13','EN');
INSERT INTO Movie_information VALUES
('M006','Saiyaara',            13.99,'Romance',  2, 3.0, DATE '2025-04-23',180,'PG-13','EN');

------------------------------------------------------------
-- MOVIE_COPY + INVENTORY_COPY_DETAIL
------------------------------------------------------------
PROMPT === MOVIE COPIES + INVENTORY DETAILS POPULATED ===

-- Insert Movie_copy and then Inventory_Copy_Detail for each copy

INSERT INTO Movie_copy VALUES ('AVG01', 'M001');
INSERT INTO Inventory_Copy_Detail VALUES ('AVG01', '4K', 'AVAILABLE');

INSERT INTO Movie_copy VALUES ('AVG02', 'M001');
INSERT INTO Inventory_Copy_Detail VALUES ('AVG02', '1080P', 'RENTED');

INSERT INTO Movie_copy VALUES ('AVG03', 'M001');
INSERT INTO Inventory_Copy_Detail VALUES ('AVG03', '1080P', 'AVAILABLE');

INSERT INTO Movie_copy VALUES ('AVG04', 'M001');
INSERT INTO Inventory_Copy_Detail VALUES ('AVG04', '720P', 'RESERVED');


INSERT INTO Movie_copy VALUES ('SPI05','M002');
INSERT INTO Inventory_Copy_Detail VALUES ('SPI05','1080P','AVAILABLE');

INSERT INTO Movie_copy VALUES ('SPI06','M002');
INSERT INTO Inventory_Copy_Detail VALUES ('SPI06','4K','RENTED');

INSERT INTO Movie_copy VALUES ('SPI07','M002');
INSERT INTO Inventory_Copy_Detail VALUES ('SPI07','480P','AVAILABLE');


INSERT INTO Movie_copy VALUES ('PARA08','M003');
INSERT INTO Inventory_Copy_Detail VALUES ('PARA08','1080P','AVAILABLE');

INSERT INTO Movie_copy VALUES ('PARA09','M003');
INSERT INTO Inventory_Copy_Detail VALUES ('PARA09','1080P','RENTED');

INSERT INTO Movie_copy VALUES ('PARA10','M003');
INSERT INTO Inventory_Copy_Detail VALUES ('PARA10','720P','AVAILABLE');


INSERT INTO Movie_copy VALUES ('IDI1','M004');
INSERT INTO Inventory_Copy_Detail VALUES ('IDI1','1080P','AVAILABLE');

INSERT INTO Movie_copy VALUES ('IDI2','M004');
INSERT INTO Inventory_Copy_Detail VALUES ('IDI2','720P','AVAILABLE');


INSERT INTO Movie_copy VALUES ('DARK1','M005');
INSERT INTO Inventory_Copy_Detail VALUES ('DARK1','4K','AVAILABLE');

INSERT INTO Movie_copy VALUES ('DARK2','M005');
INSERT INTO Inventory_Copy_Detail VALUES ('DARK2','1080P','RENTED');

INSERT INTO Movie_copy VALUES ('DARK3','M005');
INSERT INTO Inventory_Copy_Detail VALUES ('DARK3','1080P','AVAILABLE');

INSERT INTO Movie_copy VALUES ('DARK4','M005');
INSERT INTO Inventory_Copy_Detail VALUES ('DARK4','480P','AVAILABLE');


INSERT INTO Movie_copy VALUES ('SAIY1','M006');
INSERT INTO Inventory_Copy_Detail VALUES ('SAIY1','1080P','AVAILABLE');

INSERT INTO Movie_copy VALUES ('SAIY2','M006');
INSERT INTO Inventory_Copy_Detail VALUES ('SAIY2','720P','AVAILABLE');

------------------------------------------------------------
-- CUSTOMER TABLES
------------------------------------------------------------
PROMPT === CUSTOMER TABLES POPULATED ===

-- SECURITY
INSERT INTO Customer_security_info VALUES
('alice',10.00,'passAlice','Alice','Nguyen');
INSERT INTO Customer_security_info VALUES
('bob',  5.50,'passBob',  'Bob','Singh');
INSERT INTO Customer_security_info VALUES
('carol',20.00,'passCarol','Carol','Perez');
INSERT INTO Customer_security_info VALUES
('dave', 0.00,'passDave','Dave','Kim');
INSERT INTO Customer_security_info VALUES
('eve', 14.25,'passEve','Eve','Rahman');

-- PUBLIC
INSERT INTO Customer_public_info VALUES
('alice@gmail.com','Alice','Nguyen',22,'+1-416-555-1001');
INSERT INTO Customer_public_info VALUES
('bob@gmail.com','Bob','Singh',25,'+1-416-555-1002');
INSERT INTO Customer_public_info VALUES
('carol@gmail.com','Carol','Perez',31,'+1-416-555-1003');
INSERT INTO Customer_public_info VALUES
('dave@gmail.com','Dave','Kim',19,'+1-416-555-1004');
INSERT INTO Customer_public_info VALUES
('eve@gmail.com','Eve','Rahman',27,'+1-416-555-1005');

------------------------------------------------------------
-- BORROW (OLD LIBRARY)
------------------------------------------------------------
PROMPT === BORROW POPULATED ===

INSERT INTO Borrow (Copy_ID, Username, Start_Date, Returned_On)
VALUES ('AVG02','bob', DATE '2025-09-24', NULL);

INSERT INTO Borrow (Copy_ID, Username, Start_Date, Returned_On) VALUES
('SPI06','alice', DATE '2025-09-10', DATE '2025-09-12');

INSERT INTO Borrow (Copy_ID, Username, Start_Date, Returned_On) VALUES
('PARA09','dave', DATE '2025-09-15', NULL);

INSERT INTO Borrow (Copy_ID, Username, Start_Date, Returned_On) VALUES
('DARK2','eve', DATE '2025-09-26', NULL);

INSERT INTO Borrow (Copy_ID, Username, Start_Date, Returned_On) VALUES
('IDI1','carol', DATE '2025-09-18', DATE '2025-09-20');

INSERT INTO Borrow (Copy_ID, Username, Start_Date, Returned_On) VALUES
('AVG03','alice', DATE '2025-09-01', DATE '2025-09-04');

------------------------------------------------------------
-- CONTENT MANAGER
------------------------------------------------------------
PROMPT === CONTENT MANAGER POPULATED ===

INSERT INTO Employee_info_CM VALUES
('51090','charlie@gmail.com','charlie123');
INSERT INTO CM_movie_to_change VALUES
('charlie@gmail.com','M003'); -- Parasite

INSERT INTO Employee_info_CM VALUES
('52091','diana@gmail.com','diana456');
INSERT INTO CM_movie_to_change VALUES
('diana@gmail.com',NULL); -- Titanic not in schema

INSERT INTO Employee_info_CM VALUES
('53092','edward@gmail.com','edward789');
INSERT INTO CM_movie_to_change VALUES
('edward@gmail.com',NULL); -- Inception not in schema

------------------------------------------------------------
-- CUSTOMER SERVICE STAFF
------------------------------------------------------------
PROMPT === CUSTOMER SERVICE POPULATED ===

INSERT INTO Employee_info_customer_service VALUES
('60001','Josh@gmail.com','Josh123');
INSERT INTO Shift_info_customer_service VALUES
('Josh@gmail.com','Morning');

INSERT INTO Employee_info_customer_service VALUES
('60002','Zach@gmail.com','Zach223');
INSERT INTO Shift_info_customer_service VALUES
('Zach@gmail.com','Afternoon');

INSERT INTO Employee_info_customer_service VALUES
('60003','Pokemon@gmail.com','Pokemon223');
INSERT INTO Shift_info_customer_service VALUES
('Pokemon@gmail.com','Night');

------------------------------------------------------------
-- DEVELOPERS
------------------------------------------------------------
PROMPT === DEVELOPER POPULATED ===

INSERT INTO Developer_main VALUES
('70001','https://github.com/zach1','Jelly@gmail.com','Python123');
INSERT INTO Developer_speciality VALUES
('Jelly@gmail.com','https://github.com/zach1','BACKEND');

INSERT INTO Developer_main VALUES
('70002','https://github.com/Jaiden2','Jaiden@gmail.com','HTML123');
INSERT INTO Developer_speciality VALUES
('Jaiden@gmail.com','https://github.com/Jaiden2','FRONTEND');

------------------------------------------------------------
-- COMPACT_REVIEW
------------------------------------------------------------
PROMPT === REVIEWS POPULATED ===

INSERT INTO Compact_Review (Username, Movie_ID, Rating, Review_Text, Created_At)
VALUES ('alice','M001',4,'Amazing movie with great action scenes!', DATE '2025-09-05');

INSERT INTO Compact_Review (Username, Movie_ID, Rating, Review_Text, Created_At)
VALUES ('bob','M002',5,'A beautiful and enchanting film.', DATE '2025-09-15');

COMMIT;
EXIT;
