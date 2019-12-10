-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 10, 2019 at 09:50 AM
-- Server version: 5.7.28-0ubuntu0.19.04.2
-- PHP Version: 7.2.24-0ubuntu0.19.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mia`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `noofpatients` (IN `id` VARCHAR(45), OUT `nocount` VARCHAR(45))  BEGIN
select count(*) into nocount from Patient where Doc_Id = id ;
END$$

--
-- Functions
--
CREATE DEFINER=`root`@`localhost` FUNCTION `slotIsAvailable` (`doctorID` INT, `slotStartDateTime` DATETIME, `slotEndDateTime` DATETIME) RETURNS TINYINT(1) BEGIN
    RETURN CASE WHEN EXISTS (
        -- This table will contain records iff the slot clashes with an existing appointment        SELECT TRUE
        FROM Appointment AS a
        WHERE
                CONVERT(slotStartDateTime, TIME) < a.endTime   -- These two conditions will both hold iff the slot overlaps            AND CONVERT(slotEndDateTime,   TIME) > a.startTime -- with the existing appointment that it's being compared to            AND a.doctorID = doctorID
            AND a.date = CONVERT(slotStartDateTime, DATE)
    ) THEN FALSE ELSE TRUE
    END;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `Appointment`
--

CREATE TABLE `Appointment` (
  `doctorID` varchar(45) NOT NULL,
  `date` date NOT NULL,
  `startTime` time NOT NULL,
  `endTime` time NOT NULL,
  `Pat_id` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Appointment`
--

INSERT INTO `Appointment` (`doctorID`, `date`, `startTime`, `endTime`, `Pat_id`) VALUES
('123', '2019-10-06', '09:20:00', '09:30:00', '1234'),
('123', '2019-10-06', '09:40:00', '09:50:00', '1234'),
('123', '2019-10-06', '11:00:00', '11:20:00', '1234'),
('123', '2019-10-06', '11:20:00', '11:40:00', '1234'),
('123', '2019-10-06', '11:40:00', '12:00:00', '1234'),
('123', '2019-10-06', '13:00:00', '14:00:00', '1234'),
('123', '2019-10-06', '16:00:00', '16:40:00', '1234'),
('123', '2019-11-28', '05:10:00', '05:20:00', '1234'),
('123', '2019-11-29', '11:20:00', '11:30:00', '1234'),
('123', '2019-12-09', '12:30:00', '12:40:00', '12378');

--
-- Triggers `Appointment`
--
DELIMITER $$
CREATE TRIGGER `ensureNewAppointmentsDoNotClash` BEFORE INSERT ON `Appointment` FOR EACH ROW BEGIN
    IF NOT slotIsAvailable(
        NEW.doctorID,
        CAST( CONCAT(NEW.date, ' ', NEW.startTime)  AS DATETIME ),
        CAST( CONCAT(NEW.date, ' ', NEW.endTime)    AS DATETIME )
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Appointment clashes with an existing appointment!';
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `docapt`
--

CREATE TABLE `docapt` (
  `Doc_id` varchar(45) NOT NULL,
  `Pat_id` varchar(45) DEFAULT NULL,
  `date` date NOT NULL,
  `Time` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `docapt`
--

INSERT INTO `docapt` (`Doc_id`, `Pat_id`, `date`, `Time`) VALUES
('123', '1234', '2019-02-12', '03:00'),
('123', '1234', '2019-09-23', '04:00'),
('123', '1234', '2019-12-12', '04:22'),
('123', '1234', '2017-11-01', '23:59'),
('123', '1234', '2019-10-01', '23:6');

-- --------------------------------------------------------

--
-- Table structure for table `Doctors`
--

CREATE TABLE `Doctors` (
  `Doc_id` varchar(45) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Specialization` varchar(45) NOT NULL,
  `Experience` int(11) NOT NULL,
  `Clinic` varchar(45) NOT NULL,
  `Qualification` varchar(45) NOT NULL,
  `Contact` int(11) DEFAULT NULL,
  `Patient_id` varchar(45) DEFAULT NULL,
  `Passwd` varchar(45) NOT NULL,
  `rating` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Doctors`
--

INSERT INTO `Doctors` (`Doc_id`, `Name`, `Specialization`, `Experience`, `Clinic`, `Qualification`, `Contact`, `Patient_id`, `Passwd`, `rating`) VALUES
('10340', 'Swati Chandra', 'Physician', 2, '1, Ramakrishnapuram, 49 Vilivakam, Madras', 'MBB', 2241293, '1023', '1', 3),
('10341', 'Rena', 'Children', 2, 'Bikaner', 'MBBS', 97811528, NULL, '1', 3),
('123', 'Meenakshi', 'Children', 3, 'Bangalore', 'MBBS', 2345132, '1234', '1', 3),
('1234', 'Kirti Singh Chauhan', 'Endocrinologists', 5, 'Navi Road Mumbai', 'MBBS', 244675, '123', '1', 2),
('723', 'Ram S', 'Cardiologist', 10, 'Sudershana nagar , Meerut', 'MBBS', 2251723, '123', '1', 1);

--
-- Triggers `Doctors`
--
DELIMITER $$
CREATE TRIGGER `Doctors_BEFORE_INSERT` BEFORE INSERT ON `Doctors` FOR EACH ROW BEGIN
if new.Experience > 5 then
set new.rating = 1; 
else if new.Experience <=5 AND new.Experience>1 then
set new.rating = 2;
else 
set new.rating = 3; 
end if; 
end if; 
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `Drugs`
--

CREATE TABLE `Drugs` (
  `Drug_name` varchar(45) NOT NULL,
  `Disease` varchar(45) NOT NULL,
  `Shop_id` varchar(45) DEFAULT NULL,
  `company` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Drugs`
--

INSERT INTO `Drugs` (`Drug_name`, `Disease`, `Shop_id`, `company`) VALUES
('Dolapower', 'fever', '125', 'monticope'),
('Montelocast', 'anti-alergy', '123', 'monticope'),
('paracetamol', 'fever', '124', 'monticope'),
('Solvin Cold', 'Cold', '123', 'monticope');

-- --------------------------------------------------------

--
-- Table structure for table `Patient`
--

CREATE TABLE `Patient` (
  `Pat_id` varchar(45) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Contact` int(11) DEFAULT NULL,
  `Insurance_id` varchar(45) NOT NULL,
  `Medical_info` varchar(45) DEFAULT NULL,
  `Doc_Id` varchar(45) DEFAULT NULL,
  `passwd` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Patient`
--

INSERT INTO `Patient` (`Pat_id`, `Name`, `Contact`, `Insurance_id`, `Medical_info`, `Doc_Id`, `passwd`) VALUES
('1023', 'Neha', 2241793, '19068', 'HayFever', '10340', '1'),
('1234', 'Ali', 3456216, '12345', 'Fungi Infection', '123', '1'),
('12378', 'Grace', 97811529, '15152', 'fracture', '10341', '1'),
('1256', 'Sameer', 234567, '12363', 'Diabetes', '123', '1'),
('1278', 'Anajali', 2241907, '12367', 'Dialysis', '123', '1');

-- --------------------------------------------------------

--
-- Table structure for table `Retailer`
--

CREATE TABLE `Retailer` (
  `licence` varchar(45) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Address` varchar(45) DEFAULT NULL,
  `owner` varchar(45) NOT NULL,
  `passwd` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Retailer`
--

INSERT INTO `Retailer` (`licence`, `Name`, `Address`, `owner`, `passwd`) VALUES
('123', 'Chauhan Medicals', 'Bangalore', 'SPS Chauhan', '1'),
('124', 'Divine Meds', 'Hyderbad', 'Akhil Gupta', '1'),
('125', 'Life Meds', 'Bangalore', 'Rumi R', '1'),
('126', 'Gupta Store', 'Bangalore', 'Mitesh Gupta', '1'),
('127', 'Happy Meds', 'Bangalore', 'Sarvesh', '1');

-- --------------------------------------------------------

--
-- Table structure for table `Stock`
--

CREATE TABLE `Stock` (
  `Shop_id` varchar(45) DEFAULT NULL,
  `Drug` varchar(45) NOT NULL,
  `price` int(11) NOT NULL,
  `quantity` int(10) DEFAULT NULL,
  `date` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Stock`
--

INSERT INTO `Stock` (`Shop_id`, `Drug`, `price`, `quantity`, `date`) VALUES
('126', 'Dolapower', 120, 10, '2019-12-07 17:35:17'),
('123', 'Montelocast', 120, 7, '2019-12-07 17:39:56'),
('124', 'paracetamol', 32, 20, '2019-12-07 17:35:17'),
('123', 'Solvin Cold', 30, 7, '2019-12-07 17:35:17'),
('127', 'Solvin Cold', 30, 3, '2019-12-08 10:51:49');

--
-- Triggers `Stock`
--
DELIMITER $$
CREATE TRIGGER `Stock_BEFORE_INSERT` BEFORE INSERT ON `Stock` FOR EACH ROW BEGIN
set new.date  =  now();
END
$$
DELIMITER ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Appointment`
--
ALTER TABLE `Appointment`
  ADD PRIMARY KEY (`date`,`startTime`),
  ADD KEY `fk_Appointment_1_idx` (`doctorID`),
  ADD KEY `doc` (`doctorID`),
  ADD KEY `doc_id` (`doctorID`),
  ADD KEY `akp` (`doctorID`),
  ADD KEY `foreignkey` (`doctorID`),
  ADD KEY `fk` (`doctorID`),
  ADD KEY `fk_Appointment_1_idx1` (`Pat_id`);

--
-- Indexes for table `docapt`
--
ALTER TABLE `docapt`
  ADD UNIQUE KEY `time_UNIQUE` (`Time`),
  ADD KEY `fk_docapt_2_idx` (`Pat_id`),
  ADD KEY `fk_docapt_1_idx` (`Doc_id`);

--
-- Indexes for table `Doctors`
--
ALTER TABLE `Doctors`
  ADD PRIMARY KEY (`Doc_id`),
  ADD UNIQUE KEY `Contact_UNIQUE` (`Contact`);

--
-- Indexes for table `Drugs`
--
ALTER TABLE `Drugs`
  ADD PRIMARY KEY (`Drug_name`),
  ADD KEY `shop_id_idx` (`Shop_id`);

--
-- Indexes for table `Patient`
--
ALTER TABLE `Patient`
  ADD PRIMARY KEY (`Pat_id`,`Insurance_id`),
  ADD UNIQUE KEY `Contact_UNIQUE` (`Contact`),
  ADD KEY `doc_id_idx` (`Doc_Id`);

--
-- Indexes for table `Retailer`
--
ALTER TABLE `Retailer`
  ADD PRIMARY KEY (`licence`),
  ADD UNIQUE KEY `owner_UNIQUE` (`owner`);

--
-- Indexes for table `Stock`
--
ALTER TABLE `Stock`
  ADD KEY `licence_idx` (`Shop_id`),
  ADD KEY `Drug_name_idx` (`Drug`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Appointment`
--
ALTER TABLE `Appointment`
  ADD CONSTRAINT `fk` FOREIGN KEY (`doctorID`) REFERENCES `Doctors` (`Doc_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_Appointment_1` FOREIGN KEY (`Pat_id`) REFERENCES `Patient` (`Pat_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `docapt`
--
ALTER TABLE `docapt`
  ADD CONSTRAINT `fk_docapt_1` FOREIGN KEY (`Doc_id`) REFERENCES `Doctors` (`Doc_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_docapt_2` FOREIGN KEY (`Pat_id`) REFERENCES `Patient` (`Pat_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `Drugs`
--
ALTER TABLE `Drugs`
  ADD CONSTRAINT `licence` FOREIGN KEY (`Shop_id`) REFERENCES `Retailer` (`licence`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `Patient`
--
ALTER TABLE `Patient`
  ADD CONSTRAINT `doc_id` FOREIGN KEY (`Doc_Id`) REFERENCES `Doctors` (`Doc_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Stock`
--
ALTER TABLE `Stock`
  ADD CONSTRAINT `D_name` FOREIGN KEY (`Drug`) REFERENCES `Drugs` (`Drug_name`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `lic` FOREIGN KEY (`Shop_id`) REFERENCES `Retailer` (`licence`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
