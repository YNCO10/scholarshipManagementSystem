-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 15, 2025 at 03:46 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `scholarship_management_sys_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `email` varchar(200) NOT NULL,
  `pass_word` varchar(255) NOT NULL,
  `date_joined` date DEFAULT curdate(),
  `verified` tinyint(1) DEFAULT 0,
  `verify_token` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `name`, `email`, `pass_word`, `date_joined`, `verified`, `verify_token`) VALUES
(15, 'Yanco Kamphandule', 'yanco@gmail.com', '$2y$10$Hb8npJkLF/q.fYtKRkTvSuaeN0Q.wdn6WcRlfDHADF7cmCNJoXpiS', '2025-08-19', 0, NULL),
(16, 'Jeff', 'kush@gmail.com', '$2y$10$SM6md.TvrA6SCBhOXZfBWO7FnYFAtRDLyvzQO10kntlhh/s4ErL1m', '2025-08-20', 0, NULL),
(17, 'mtendere Kamphandule', 'mtende@gmail.com', '$2y$10$UGxHR/wsVqRqJacdsS9F9.tAeG8MQJ8IHkLKhBv32OnjLrLkb14Fa', '2025-08-23', 0, NULL),
(18, 'Ipyana Applicant', 'ipyana@gmail.com', '$2y$10$MAezR2881K5H71PVOI/fkOQNgaXHj.ZfJYfSqL2drZCDQZu.FmPL2', '2025-08-23', 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `applicant`
--

CREATE TABLE `applicant` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `email` varchar(200) NOT NULL,
  `pass_word` varchar(255) NOT NULL,
  `age` int(11) NOT NULL,
  `phone_num` varchar(25) NOT NULL,
  `gender` varchar(15) NOT NULL,
  `reviewer_id` int(11) DEFAULT NULL,
  `is_accepted` tinyint(1) DEFAULT 0,
  `nationality` varchar(70) DEFAULT NULL,
  `education_level` varchar(100) DEFAULT NULL,
  `dob` date NOT NULL,
  `verified` tinyint(1) DEFAULT 0,
  `verify_token` varchar(64) DEFAULT NULL,
  `subject` varchar(50) DEFAULT NULL,
  `assessment_completed` tinyint(1) DEFAULT 0,
  `date_registered` date DEFAULT curdate(),
  `score` int(11) DEFAULT 0,
  `gpa` int(11) DEFAULT NULL,
  `school_attended` varchar(100) DEFAULT NULL,
  `income_bracket` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `applicant`
--

INSERT INTO `applicant` (`id`, `name`, `email`, `pass_word`, `age`, `phone_num`, `gender`, `reviewer_id`, `is_accepted`, `nationality`, `education_level`, `dob`, `verified`, `verify_token`, `subject`, `assessment_completed`, `date_registered`, `score`, `gpa`, `school_attended`, `income_bracket`) VALUES
(1, 'Test Applicant 2', 'test2@gmail.com', '$2y$10$wTvYJG9EfJsEIl8BO0DtkeAu4VTpY4jTfOqnxQAA1kPmjKFj45wwa', 18, '+265881000002', 'Female', NULL, 0, 'Malawian', 'Diploma', '2003-02-12', 0, NULL, 'Business & Management', 0, '2025-09-22', 32, 5, "Chichiri Secondary School", "Between MWK1,000,000 - MWK2,000,000"),
(2, 'Test Applicant 3', 'test3@gmail.com', '$2y$10$wIugeGF.J5nvc7PXs5pT..Tm5k4qQcZ6bUToy/5QSPaZ.FYhNFDuK', 24, '+265881000003', 'Female', NULL, 0, 'Zimbabwe', 'Diploma', '2001-08-09', 0, NULL, 'Engineering & Technology', 0, '2025-09-22', 91, 4, "Chichiri Secondary School", "Between MWK500,00 - MWK1,000,000"),
(3, 'Test Applicant 4', 'test4@gmail.com', '$2y$10$DzcmzvIyYxjDsxnUb/iijuX0Hq3A0Tchccw5PLTmc7RgoByFGpS96', 19, '+265881000004', 'Female', NULL, 0, 'Egypt', 'Secondary School', '2006-11-23', 0, NULL, 'Economics', 0, '2025-09-22', 52, 3, "Ndirande Hill Secondary", "Between MKW250,000 - MWK500,000"),
(4, 'Test Applicant 6', 'test6@gmail.com', '$2y$10$G0dU3IFMgCbk1DSgaF7/mexfQ.eiDz0TLGPlf6OyAwwWPH1zvsEFW', 23, '+265881000006', 'Male', NULL, 0, 'Zimbabwe', 'Diploma', '2002-03-30', 0, NULL, 'Law', 0, '2025-09-22', 117, 2, "Zomba Catholic Secondary", "Between MKW250,000 - MWK500,000"),
(5, 'Test Applicant 7', 'test7@gmail.com', '$2y$10$hgH6Q9exO8sqEUZcjLVVQuPpAAXN2QwUBKXzObDd7EfvXaFTBVHyW', 25, '+265881000007', 'Male', NULL, 0, 'Malawian', 'Bachelors Degree', '2000-12-05', 0, NULL, 'Psychology', 0, '2025-09-22', 86, 1, "Ndirande Hill Secondary", "less than MWK150,000"),
(6, 'Test Applicant 8', 'test8@gmail.com', '$2y$10$fBDU4gqxKh/nR8eJYsHTTubb6LGd00WHLj7dwLERGlVLINFV/z9s6', 18, '+265881000008', 'Female', NULL, 0, 'Malawian', 'Secondary School', '2007-07-07', 0, NULL, 'Computer Science & IT', 0, '2025-09-22', 48, 5, "Chichiri Secondary School", "less than MWK150,000"),
(7, 'Test Applicant 9', 'test9@gmail.com', '$2y$10$AB7xzvP.23l2ND5fp2wlWOmucPwMcQWX8905i0v.gqPCtWZyfQlCG', 27, '+265881000009', 'Male', NULL, 0, 'Tunisia', 'Masters Degree', '1998-09-02', 0, NULL, 'Business & Management', 1, '2025-09-22', 51, 4, "Bwaila Secondary School", "less than MWK150,000"),
(8, 'Test Applicant 10', 'test10@gmail.com', '$2y$10$Aka/2KXQLa8OyuLgn3B6u..Q8R1rP3Vr0kMaXYBatTkD5Er8qKDze', 26, '+265881000010', 'Female', NULL, 0, 'Malawian', 'Diploma', '1999-05-19', 0, NULL, 'Engineering & Technology', 0, '2025-09-22', 20, 3, "Bwaila Secondary School", "Between MKW250,000 - MWK500,000"),
(9, 'Test Applicant 11', 'test11@gmail.com', '$2y$10$OI/KLqdm0Qkmo0uEZLcgO.FCjTE4SPhLoZoHoDj4zrvZyB8haB.SK', 20, '+265881000011', 'Female', NULL, 0, 'Malawian', 'Secondary School', '2005-04-01', 0, NULL, 'Economics', 0, '2025-09-23', 3, 2, "Mchinji Boys Secondary", "less than MWK150,000"),
(10, 'Test Applicant 12', 'test12@gmail.com', '$2y$10$wTvYJG9EfJsEIl8BO0DtkeAu4VTpY4jTfOqnxQAA1kPmjKFj45wwa', 37, '+265881000012', 'Female', NULL, 0, 'Malawian', 'Doctorate (PhD)', '2003-02-12', 0, NULL, 'Health Sciences', 0, '2025-09-23', 118, 1, "Kamuzu Academy", "More than MWK2,000,000"),
(11, 'Test Applicant 13', 'test13@gmail.com', '$2y$10$wIugeGF.J5nvc7PXs5pT..Tm5k4qQcZ6bUToy/5QSPaZ.FYhNFDuK', 18, '+265881000013', 'Female', NULL, 0, 'Egypt', 'Diploma', '2001-08-09', 0, NULL, 'Law', 0, '2025-09-23', 84, 5, "Mchinji Boys Secondary", "Between MKW250,000 - MWK500,000"),
(12, 'Test Applicant 14', 'test14@gmail.com', '$2y$10$DzcmzvIyYxjDsxnUb/iijuX0Hq3A0Tchccw5PLTmc7RgoByFGpS96', 19, '+265881000014', 'Female', NULL, 0, 'Malawian', 'Secondary School', '2006-11-23', 0, NULL, 'Psychology', 0, '2025-09-24', 99, 4, "Chichiri Secondary School", "Between MKW250,000 - MWK500,000"),
(13, 'Test Applicant 15', 'test15@gmail.com', '$2y$10$3upKZzWQ2khWfsZkkqQ2lOqc2orqwgEq.Zxr7RmE0pv8BTBBsh.XO', 21, '+265881000015', 'Female', NULL, 0, 'Malawian', 'Diploma', '2004-06-16', 0, NULL, 'Computer Science & IT', 0, '2025-09-24', 73, 3, "Nkhotakota Secondary School", "Between MKW250,000 - MWK500,000"),
(14, 'Test Applicant 16', 'test16@gmail.com', '$2y$10$G0dU3IFMgCbk1DSgaF7/mexfQ.eiDz0TLGPlf6OyAwwWPH1zvsEFW', 23, '+265881000016', 'Male', NULL, 0, 'Tunisia', 'Doctorate (PhD)', '2002-03-30', 0, NULL, 'Business & Management', 0, '2025-09-25', 81, 2, "Mzuzu Academy", "More than MWK2,000,000"),
(15, 'Test Applicant 17', 'test17@gmail.com', '$2y$10$hgH6Q9exO8sqEUZcjLVVQuPpAAXN2QwUBKXzObDd7EfvXaFTBVHyW', 25, '+265881000017', 'Male', NULL, 0, 'South Africa', 'Bachelors Degree', '2000-12-05', 0, NULL, 'Engineering & Technology', 0, '2025-09-25', 89, 4, "Mtendere Secondary School", "Between MKW250,000 - MWK500,000"),
(16, 'Test Applicant 19', 'test19@gmail.com', '$2y$10$AB7xzvP.23l2ND5fp2wlWOmucPwMcQWX8905i0v.gqPCtWZyfQlCG', 27, '+265881000019', 'Male', NULL, 0, 'Malawian', 'Masters Degree', '1998-09-02', 0, NULL, 'Health Sciences', 0, '2025-09-25', 51, 1, "Nkhotakota Secondary School", "Between MWK150,000 - MWK250,000"),
(17, 'Test Applicant 20', 'test20@gmail.com', '$2y$10$Aka/2KXQLa8OyuLgn3B6u..Q8R1rP3Vr0kMaXYBatTkD5Er8qKDze', 20, '+265881000019', 'Female', NULL, 0, 'Tunisia', 'Masters Degree', '2005-02-08', 0, NULL, 'Health Sciences', 0, '2025-09-25', 39, 3, "Zomba Catholic Secondary", "Between MKW250,000 - MWK500,000"),
(18, 'Big Man Yanco', 'yancokampha@gmail.com', '$2y$10$OI/KLqdm0Qkmo0uEZLcgO.FCjTE4SPhLoZoHoDj4zrvZyB8haB.SK', 20, '+265881000001', 'Male', NULL, 0, 'Malawian', 'Secondary School', '2005-02-08', 1, NULL, 'Computer Science & IT', 1, '2025-10-10', 25, 2, "Mtendere Secondary School", "Between MWK150,000 - MWK250,000");

-- --------------------------------------------------------

--
-- Table structure for table `applications`
--

CREATE TABLE `applications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `scholarship_id` int(11) NOT NULL,
  `application_status` enum('REJECTED','Pending','Reviwed','ACCEPTED') NOT NULL DEFAULT 'Pending',
  `date_submitted` date DEFAULT curdate(),
  `fin_assistance` tinyint(1) NOT NULL DEFAULT 0,
  `reason_for_applying` varchar(255) DEFAULT NULL,
  `careerGoals` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `applications`
--

INSERT INTO `applications` (`id`, `user_id`, `scholarship_id`, `application_status`, `date_submitted`, `fin_assistance`, `reason_for_applying`, `careerGoals`) VALUES
(1, 1, 12, 'Pending', '2025-09-29', 1, 'I want to pursue higher education to develop skills for my community.', 'To become a teacher in rural areas.'),
(2, 2, 19, 'REJECTED', '2025-09-29', 0, 'This scholarship will allow me to complete my studies and acquire skills that will benefit both myself and my community.', 'To become a medical doctor serving rural areas.'),
(3, 3, 18, 'Pending', '2025-09-29', 1, 'I want to pursue higher education despite financial difficulties, and this scholarship will provide the chance.', 'To become a teacher who inspires and uplifts students.'),
(4, 4, 13, 'Pending', '2025-09-29', 1, 'This scholarship will help me pay for my tuition and focus fully on my studies without worrying about school fees.', 'To become a lawyer advocating for justice and equality.'),
(5, 5, 12, 'Pending', '2025-09-29', 0, 'I am eager to study but need financial support to achieve my goals.', 'To become an engineer solving real-world problems.'),
(6, 6, 17, 'Pending', '2025-09-29', 1, 'My family cannot afford to pay my school fees, and this scholarship will allow me to continue my education.', 'To become a nurse providing healthcare to underserved areas.'),
(7, 7, 12, 'Pending', '2025-09-29', 0, 'I want to study further and this scholarship will allow me to pursue my dream career.', 'To become an accountant and support businesses with financial planning.'),
(8, 8, 18, 'Pending', '2025-09-29', 1, 'Receiving this scholarship will help me overcome financial barriers and achieve academic success.', 'To become a data scientist working on innovative solutions.'),
(9, 9, 13, 'Pending', '2025-09-29', 0, 'I am motivated to learn but lack the financial resources, so this scholarship will enable me to continue.', 'To become an environmentalist promoting sustainable living.'),
(10, 10, 19, 'Pending', '2025-09-29', 1, 'I wish to achieve academic excellence but financial limitations stand in my way, hence this application.', 'To become an architect designing sustainable housing.'),
(11, 11, 13, 'Pending', '2025-09-29', 0, 'I want to pursue higher education to uplift my family and contribute positively to society.', 'To become a journalist advocating for transparency.'),
(12, 12, 17, 'Pending', '2025-09-29', 1, 'I am committed to education but lack the resources, and this scholarship will help me complete my studies.', 'To become a doctor addressing public health challenges.'),
(13, 13, 18, 'Pending', '2025-09-29', 1, 'This scholarship will reduce the financial stress my parents face and allow me to excel academically.', 'To become a lecturer inspiring future generations.'),
(14, 14, 12, 'Pending', '2025-09-29', 0, 'With this scholarship, I can continue learning and aim for a brighter future.', 'To become an entrepreneur creating job opportunities.'),
(15, 15, 13, 'Pending', '2025-09-29', 1, 'I want to improve my education and this opportunity will help me reach greater heights.', 'To become a software engineer building impactful apps.'),
(16, 16, 19, 'Pending', '2025-09-29', 0, 'Education is my passion and I seek this scholarship to support my academic journey.', 'To become a pilot with international experience.'),
(17, 17, 17, 'Pending', '2025-09-29', 1, 'I want to pursue studies in my field of interest and this scholarship is the only way.', 'To become a banker supporting economic growth.'),
(18, 18, 18, 'Pending', '2025-09-29', 1, 'I am applying for this scholarship because it is the only chance I have to advance my studies.', 'To become a scientist researching renewable energy.');

-- --------------------------------------------------------

--
-- Table structure for table `assessment`
--

CREATE TABLE `assessment` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `score` float DEFAULT 0,
  `totalQuest` int(11) DEFAULT 0,
  `date_taken` date DEFAULT curdate()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `assessment`
--

INSERT INTO `assessment` (`id`, `user_id`, `score`, `totalQuest`, `date_taken`) VALUES
(1, 1, 100, 40, '2025-10-03'),
(2, 2, 78, 40, '2025-10-03'),
(3, 3, 64, 40, '2025-10-03'),
(4, 4, 55, 40, '2025-10-03'),
(5, 5, 92, 40, '2025-10-03'),
(6, 6, 100, 40, '2025-10-03'),
(7, 7, 81, 40, '2025-10-03'),
(8, 8, 47, 40, '2025-10-03'),
(9, 9, 36, 40, '2025-10-03'),
(10, 10, 88, 40, '2025-10-03'),
(11, 11, 53, 40, '2025-10-03'),
(12, 12, 69, 40, '2025-10-03'),
(13, 13, 74, 40, '2025-10-03'),
(14, 14, 100, 40, '2025-10-03'),
(15, 15, 61, 40, '2025-10-03'),
(16, 16, 82, 40, '2025-10-03'),
(17, 17, 95, 40, '2025-10-03'),
(18, 18, 42, 40, '2025-10-03'),
(19, 19, 67, 40, '2025-10-03'),
(20, 20, 59, 40, '2025-10-03'),
(21, 21, 40, 40, '2025-10-10');

-- --------------------------------------------------------

--
-- Table structure for table `documents`
--

CREATE TABLE `documents` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `doc_type` varchar(25) DEFAULT 'unspecified',
  `date_uploaded` date DEFAULT curdate(),
  `application_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `documents`
--

INSERT INTO `documents` (`id`, `user_id`, `file_path`, `doc_type`, `date_uploaded`, `application_ID`) VALUES
(1, 1, 'uploads/doc_101.pdf', 'Transcript', '2025-09-29', 1),
(2, 2, 'uploads/doc_201.pdf', 'National ID', '2025-09-29', 12),
(3, 3, 'uploads/doc_301.pdf', 'Transcript', '2025-09-29', 1),
(4, 3, 'uploads/doc_302.pdf', 'Recommendation Letter', '2025-09-29', 2),
(5, 3, 'uploads/doc_303.pdf', 'Proof Of Need', '2025-09-29', 3),
(6, 3, 'uploads/doc_304.pdf', 'National ID', '2025-09-29', 4),
(7, 4, 'uploads/doc_401.pdf', 'Recommendation Letter', '2025-09-29', 13),
(8, 5, 'uploads/doc_501.pdf', 'Transcript', '2025-09-29', 5),
(9, 6, 'uploads/doc_601.pdf', 'Transcript', '2025-09-29', 14),
(10, 7, 'uploads/doc_701.pdf', 'Transcript', '2025-09-29', 5),
(11, 7, 'uploads/doc_702.pdf', 'Recommendation Letter', '2025-09-29', 6),
(12, 7, 'uploads/doc_703.pdf', 'Proof Of Need', '2025-09-29', 7),
(13, 7, 'uploads/doc_704.pdf', 'National ID', '2025-09-29', 8),
(14, 8, 'uploads/doc_801.pdf', 'National ID', '2025-09-29', 15),
(15, 9, 'uploads/doc_901.pdf', 'Transcript', '2025-09-29', 16),
(16, 9, 'C:\\XAMPP\\htdocs\\BackEnd\\scholarshipManagement\\application/docs/uploadedFiles/1760080010_myAssignment.pdf', 'Transcript', '2025-10-10', NULL),
(17, 9, 'C:\\XAMPP\\htdocs\\BackEnd\\scholarshipManagement\\application/docs/uploadedFiles/1760080010_Network Security and Cryptography Student Guide.pdf', 'National_ID', '2025-10-10', NULL),
(18, 9, 'C:\\XAMPP\\htdocs\\BackEnd\\scholarshipManagement\\application/docs/uploadedFiles/1760080010_AD ASSIGNMENT.pdf', 'Recommendation_Letter', '2025-10-10', NULL),
(19, 9, 'C:\\XAMPP\\htdocs\\BackEnd\\scholarshipManagement\\application/docs/uploadedFiles/1760080010_mySignature.pdf', 'Proof_Of_Need', '2025-10-10', NULL),
(20, 10, 'uploads/doc_1001.pdf', 'Recommendation Letter', '2025-09-29', 17),
(21, 11, 'uploads/doc_1101.pdf', 'Proof Of Need', '2025-09-29', 18),
(22, 12, 'uploads/doc_1201.pdf', 'Transcript', '2025-09-29', 9),
(23, 12, 'uploads/doc_1202.pdf', 'Recommendation Letter', '2025-09-29', 10),
(24, 12, 'uploads/doc_1203.pdf', 'Proof Of Need', '2025-09-29', 11),
(25, 13, 'uploads/doc_1301.pdf', 'Transcript', '2025-09-29', 18),
(26, 14, 'uploads/doc_1401.pdf', 'Recommendation Letter', '2025-09-29', 1),
(27, 15, 'uploads/doc_1501.pdf', 'National ID', '2025-09-29', 2),
(28, 16, 'uploads/doc_1601.pdf', 'Transcript', '2025-09-29', 3),
(29, 17, 'uploads/doc_1701.pdf', 'Recommendation Letter', '2025-09-29', 4),
(30, 18, 'uploads/doc_1801.pdf', 'Proof Of Need', '2025-09-29', 18);

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `msg` varchar(200) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `sender_name` varchar(150) NOT NULL,
  `recipient_name` varchar(150) NOT NULL,
  `recipient_email` varchar(200) NOT NULL,
  `noti_status` varchar(10) DEFAULT 'unseen',
  `date_sent` date DEFAULT curdate(),
  `date_seen` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `title`, `msg`, `sender_id`, `sender_name`, `recipient_name`, `recipient_email`, `noti_status`, `date_sent`, `date_seen`) VALUES
(1, 'Application Denied', 'We are sorry to inform you that you have NOT been accepted. Please feel free to Apply for the next scholarship', 15, 'Yankho K', 'Dennis', 'yancokampha@gmail.com', 'seen', '2025-09-19', '2025-10-11'),
(2, 'Application Accepted.', 'Congratulations, You have been accepted!', 15, 'Yankho K', 'Dennis', 'yancokampha@gmail.com', 'seen', '2025-09-19', '2025-10-11'),
(3, 'Notification Successful', 'You have successfully sent your First notification.', 15, 'Yankho K', 'Dennis', 'yancokampha@gmail.com', 'unseen', '2025-09-19', NULL),
(4, 'Notification Successful', 'You have successfully sent your First notification.', 15, 'Yankho K', 'Dennis', 'yancokampha@gmail.com', 'seen', '2025-09-19', '2025-10-13'),
(5, 'Information About Nacit', 'This might not be the last time you are seeing this.', 15, 'Yankho K', 'Dennis', 'yancokampha@gmail.com', 'seen', '2025-09-23', '2025-10-11'),
(6, 'Information About Scholarship', 'We are sorry to inform you that you have NOT been accepted. Please feel free to Apply for the next scholarship', 15, 'Yankho K', 'Dennis', 'yancokampha@gmail.com', 'seen', '2025-09-23', '2025-10-11'),
(7, 'Hey', 'Intrusion Detection Systems (IDSs) are important because they monitor network or host activities to detect malicious behavior early. A Network based IDS (NIDS) mostly placed between the router and int', 15, 'Yanco Kamphandule', 'Big Man Yanco', 'yancokampha@gmail.com', 'unseen', '2025-10-13', NULL),
(8, 'Hello yankho', 'We are sorry to inform you that you have NOT been accepted. Please feel free to Apply for the next scholarship', 15, 'Yanco Kamphandule', 'Big Man Yanco', 'yancokampha@gmail.com', 'unseen', '2025-10-13', NULL),
(9, 'Hello yankho', 'Intrusion Detection Systems (IDSs) are important because they monitor network or host activities to detect malicious behavior early. A Network based IDS (NIDS) mostly placed between the router and int', 15, 'Yanco Kamphandule', 'Big Man Yanco', 'yancokampha@gmail.com', 'unseen', '2025-10-13', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `perks`
--

CREATE TABLE `perks` (
  `perk_id` int(11) NOT NULL,
  `perk_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `perks`
--

INSERT INTO `perks` (`perk_id`, `perk_name`) VALUES
(2, 'Insurance'),
(3, 'Travel Allowance'),
(4, 'Job Opportunities'),
(5, 'Accommodation'),
(6, 'Workshop Access');

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `id` int(11) NOT NULL,
  `category` varchar(30) NOT NULL,
  `question_txt` varchar(200) NOT NULL,
  `option_a` text DEFAULT NULL,
  `option_b` text DEFAULT NULL,
  `option_c` text DEFAULT NULL,
  `option_d` text DEFAULT NULL,
  `ans` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`id`, `category`, `question_txt`, `option_a`, `option_b`, `option_c`, `option_d`, `ans`) VALUES
(47, 'numerical', 'An item priced at $80 is increased by 15% and then decreased by 20% of the new price. What is the final price?', 'MWK72.00', 'MWK73.60', 'MWK74.00', 'MWK76.00', 'b'),
(48, 'numerical', 'If A:B = 2:3 and B:C = 5:4, what is A:C?', '3.50', '5.6', '6.5', '4.5', 'b'),
(49, 'numerical', 'A 120 m long train passes a pole in 9 seconds. What is its speed (km/h)?', '40', '45', '48', '54', 'c'),
(50, 'numerical', 'Find the simple interest on MWK2,500 at 6% per annum for 3 years.', 'MWK360', 'MWK420', 'MWK450', 'MWK540', 'c'),
(51, 'numerical', 'Which is the largest fraction?', '  5/12', '  3/7 ', '  7/15', '  4/9 ', 'c'),
(52, 'numerical', 'Find the next term: 2, 6, 12, 20, 30, ?', '38', '40', '42', '44', 'c'),
(53, 'numerical', 'A can complete a job in 12 days and B in 18 days. Working together, how many days to finish the job?', '6 days', '7.2 days', '8 days', '9 days', 'b'),
(54, 'numerical', 'A phone bought for MWK240 is sold at a 25% loss. What is the selling price?', 'MWK150', 'MWK170', 'MWK180', 'MWK200', 'c'),
(55, 'numerical', 'Company sales (thousand units): Q1=320, Q2=400, Q3=360, Q4=440. What is the % increase from Q1 to Q4?', '25.0%', '33.3%', '37.5%', '40.0%', 'c'),
(56, 'numerical', 'How many 3-digit numbers can be formed from digits 1–5, without repetition, that are even?', '12', '18', '20', '24', 'd'),
(57, 'numerical', 'Class A average = 72 (25 students), Class B average = 68 (35 students). Combined average?', '69.2', '69.5', '69.6', '70', 'c'),
(58, 'numerical', 'Pipe A fills a tank in 12 h, B in 15 h; drain C empties in 20 h. All opened together. Time to fill?', '8 h', '9 h', '10 h', '12 h ', 'c'),
(59, 'numerical', 'Solve for x: 8^x = 32.', '1.5', '5/3', '7/4', '2', 'b'),
(60, 'numerical', 'If $1 = MWK 1700, how many dollars equal MWK 510,000?', '$250', '$300', '$350', '$380', 'b'),
(61, 'numerical', 'The sum of two numbers is 50 and their difference is 14. What is the larger number?', '18', '28', '32', '36', 'c'),
(62, 'numerical', 'From a standard 52-card deck, what is the probability of drawing a King or a Queen?', '1/13', '2/13', '3/26', '4/13', 'b'),
(63, 'numerical', 'The ratio of present ages of X and Y is 4:5. If their sum is 45, what is X’s age?', '16', '18', '20', '24', 'c'),
(64, 'numerical', 'Fill the missing term: 1, 3, 9, 27, ?, 243', '54', '72', '81', '90', 'c'),
(65, 'numerical', 'Find the compound interest on MWK5,000 at 8% per annum for 2 years (compounded annually).', 'MWK800', 'MWK816', 'MWK832', 'MWK864', 'c'),
(66, 'numerical', 'After a 20% discount, the sale price is $144. What was the original price?', 'MWK160', 'MWK170', 'MWK175', 'MWK180', 'd'),
(191, 'verbal', 'Choose the word most opposite in meaning to benevolent.', 'A. Kind', 'B. Generous', 'C. Cruel', 'D. Helpful', 'c'),
(192, 'verbal', 'Complete the sentence: She was so tired that she could hardly ___ her eyes open.', 'A. keep', 'B. leave', 'C. make', 'D. force', 'a'),
(193, 'verbal', 'Which word is most similar in meaning to transparent?', 'A. Opaque', 'B. Clear', 'C. Solid', 'D. Hidden', 'b'),
(194, 'verbal', 'Identify the error: “He don’t like playing football.”', 'A. He', 'B. don’t', 'C. playing', 'D. football', 'b'),
(195, 'verbal', 'Rearrange the words to form a meaningful sentence: “quickly / the / ran / dog / very”', 'A. Very the dog ran quickly', 'B. The dog ran very quickly', 'C. The quickly ran dog very', 'D. Quickly ran the dog very', 'b'),
(196, 'verbal', 'Choose the correct analogy: Book : Reading :: Knife : ?', 'A. Writing', 'B. Drawing', 'C. Cutting', 'D. Cooking', 'c'),
(197, 'verbal', 'Select the correct spelling:', 'A. Occured', 'B. Occurred', 'C. Ocurred', 'D. Ocurreded', 'b'),
(198, 'verbal', 'Which of the following is a synonym for abundant?', 'A. Scarce', 'B. Plentiful', 'C. Rare', 'D. Few', 'b'),
(199, 'verbal', 'Find the odd one out:', 'A. Apple', 'B. Mango', 'C. Banana', 'D. Potato', 'd'),
(200, 'verbal', 'Choose the word that best completes the sentence: “The soldiers fought bravely ___ their country.”', 'A. of', 'B. by', 'C. for', 'D. with', 'c'),
(201, 'verbal', 'Choose the correct word: The teacher asked us to be ___ while she explained.', 'A. quit', 'B. quiet', 'C. quite', 'D. quoit', 'b'),
(202, 'verbal', 'Which word does not belong?', 'A. Laugh', 'B. Smile', 'C. Cry', 'D. Run', 'd'),
(203, 'verbal', 'Fill in the blank: “He succeeded ___ his hard work.”', 'A. because', 'B. because of', 'C. due', 'D. for', 'b'),
(204, 'verbal', 'Which of these is the correct passive form? “They are cleaning the room.”', 'A. The room is cleaned by them.', 'B. The room is being cleaned.', 'C. The room cleans itself.', 'D. The room has been cleaned.', 'b'),
(205, 'verbal', 'Choose the correctly punctuated sentence:', 'A. She said “I am ready”.', 'B. She said, “I am ready.”', 'C. She said “I am ready.”', 'D. She said, I am ready.', 'b'),
(206, 'verbal', 'Which phrase best replaces the underlined part? “She was over the moon after passing the exam.”', 'A. Sad', 'B. Very happy', 'C. Tired', 'D. Angry', 'b'),
(207, 'verbal', 'Which word is the best fit? “Even though he was tired, he kept working ___.”', 'A. lazily', 'B. hardly', 'C. diligently', 'D. slowly', 'c'),
(208, 'verbal', 'Which of the following is a one-word substitute for “a person who writes poems”?', 'A. Poet', 'B. Author', 'C. Writer', 'D. Novelist', 'a'),
(209, 'verbal', 'Which sentence is grammatically correct?', 'A. She don’t like mangoes.', 'B. She doesn’t likes mangoes.', 'C. She doesn’t like mangoes.', 'D. She not like mangoes.', 'c'),
(210, 'verbal', 'Select the best conclusion: “All athletes are disciplined. John is an athlete.”', 'A. John is not disciplined.', 'B. John may be disciplined.', 'C. John is disciplined.', 'D. John dislikes discipline.', 'c'),
(273, 'logical', 'Find the next number in the series: 2, 4, 8, 16, ?', 'A. 18', 'B. 24', 'C. 32', 'D. 36', 'c'),
(274, 'logical', 'Which is the odd one out?', 'A. Square', 'B. Circle', 'C. Triangle', 'D. Cube', 'd'),
(275, 'logical', 'If CAT = 3120 (C=3, A=1, T=20), then DOG = ?', 'A. 4157', 'B. 4715', 'C. 4627', 'D. 4782', 'b'),
(276, 'logical', 'All cats are animals. Some animals are not dogs. Conclusion: Some cats are not dogs. Is the conclusion valid?', 'A. Yes', 'B. No', 'C. Cannot say', 'D. Only sometimes', 'a'),
(277, 'logical', 'If TABLE = 52 and CHAIR = 43, then BENCH = ?', 'A. 40', 'B. 41', 'C. 42', 'D. 44', 'c'),
(278, 'logical', 'Which number should replace the question mark? 5, 10, 20, 40, ?', 'A. 50', 'B. 60', 'C. 70', 'D. 80', 'd'),
(279, 'logical', 'Which pair does not belong?', 'A. Pen : Write', 'B. Knife : Cut', 'C. Book : Read', 'D. Spoon : Eat', 'd'),
(280, 'logical', 'Which is the odd one out?', 'A. Red', 'B. Green', 'C. Yellow', 'D. Square', 'd'),
(281, 'logical', 'A is older than B. B is older than C. Who is the youngest?', 'A. A', 'B. B', 'C. C', 'D. Cannot say', 'c'),
(282, 'logical', 'If South becomes North, East becomes West, and so on, then what will West become?', 'A. East', 'B. North', 'C. South', 'D. Same', 'd'),
(283, 'logical', 'Which number is missing? 3, 6, 12, 24, ?', 'A. 36', 'B. 48', 'C. 60', 'D. 72', 'b'),
(284, 'logical', 'Choose the correct analogy: Finger : Hand :: Toe : ?', 'A. Foot', 'B. Leg', 'C. Shoe', 'D. Nail', 'a'),
(285, 'logical', 'Pointing to a man, Sarah says: “He is the son of my grandfather’s only son.” Who is the man?', 'A. Her uncle', 'B. Her brother', 'C. Her cousin', 'D. Her father', 'b'),
(286, 'logical', 'If all roses are flowers and some flowers fade quickly, what can be concluded?', 'A. Some roses fade quickly', 'B. All flowers are roses', 'C. Some flowers are not roses', 'D. Cannot be determined', 'd'),
(287, 'logical', 'Arrange the words logically: 1. Seed 2. Plant 3. Fruit 4. Tree 5. Flower', 'A. 1,2,3,4,5', 'B. 1,2,4,5,3', 'C. 2,1,4,3,5', 'D. 3,1,2,5,4', 'b'),
(288, 'logical', 'Find the odd one out: 2, 6, 12, 20, 30', 'A. 2', 'B. 6', 'C. 20', 'D. 30', 'c'),
(289, 'logical', 'Which number is next? 1, 4, 9, 16, ?', 'A. 20', 'B. 21', 'C. 25', 'D. 36', 'c'),
(290, 'logical', 'If MONKEY is coded as NLPLOFZ, then DONKEY will be coded as?', 'A. EPOLEZ', 'B. DPOLEZ', 'C. EPNLFZ', 'D. EPOLEF', 'a'),
(291, 'logical', 'Two men start walking in opposite directions. One walks 5 km, the other 7 km. What is the distance between them?', 'A. 10 km', 'B. 11 km', 'C. 12 km', 'D. 13 km', 'b'),
(292, 'logical', 'If it takes 5 machines 5 minutes to make 5 items, how many minutes will it take 100 machines to make 100 items?', 'A. 1', 'B. 5', 'C. 10', 'D. 20', 'b'),
(335, 'critical', 'If evidence contradicts your belief, should you re-evaluate your belief?', 'Yes', 'No', '', '', 'a'),
(336, 'critical', 'Can two people look at the same set of facts and reach different valid conclusions?', 'Yes', 'No', '', '', 'a'),
(337, 'critical', 'If an argument has false premises, can it still be valid?', 'Yes', 'No', '', '', 'b'),
(338, 'critical', 'Does correlation always imply causation?', 'Yes', 'No', '', '', 'b'),
(339, 'critical', 'Should you question the source of information before accepting it?', 'Yes', 'No', '', '', 'a'),
(340, 'critical', 'If a conclusion is based on assumptions, should the assumptions be examined?', 'Yes', 'No', '', '', 'a'),
(341, 'critical', 'Can a strong argument have a false conclusion?', 'Yes', 'No', '', '', 'a'),
(342, 'critical', 'Does anecdotal evidence count as strong proof in critical reasoning?', 'Yes', 'No', '', '', 'b'),
(343, 'critical', 'Is it possible for a valid argument to be unsound?', 'Yes', 'No', '', '', 'a'),
(344, 'critical', 'If new evidence arises, should it change how you interpret old data?', 'Yes', 'No', '', '', 'a'),
(345, 'critical', 'Should personal bias be considered when evaluating arguments?', 'Yes', 'No', '', '', 'a'),
(346, 'critical', 'If two statements contradict each other, can both be true?', 'Yes', 'No', '', '', 'b'),
(347, 'critical', 'Is it necessary to identify assumptions in everyday reasoning?', 'Yes', 'No', '', '', 'a'),
(348, 'critical', 'Can a logically valid argument still mislead people?', 'Yes', 'No', '', '', 'a'),
(349, 'critical', 'Does the credibility of a source affect the strength of its argument?', 'Yes', 'No', '', '', 'a'),
(350, 'critical', 'If an argument appeals to emotions, is it always weak?', 'Yes', 'No', '', '', 'b'),
(351, 'critical', 'Can an argument be logical but still unethical?', 'Yes', 'No', '', '', 'a'),
(352, 'critical', 'Does more evidence always mean stronger reasoning?', 'Yes', 'No', '', '', 'b'),
(353, 'critical', 'If a statement is popular, does that make it true?', 'Yes', 'No', '', '', 'b'),
(354, 'critical', 'Is critical thinking useful in everyday decision making?', 'Yes', 'No', '', '', 'a'),
(355, 'critical', 'If a conclusion does not follow from the premises, is the argument invalid?', 'Yes', 'No', '', '', 'a'),
(356, 'critical', 'Should alternative explanations always be considered before accepting a conclusion?', 'Yes', 'No', '', '', 'a'),
(357, 'critical', 'If one strong piece of evidence conflicts with many weak ones, should it be prioritized?', 'Yes', 'No', '', '', 'a'),
(358, 'critical', 'Can persuasive language make a weak argument seem strong?', 'Yes', 'No', '', '', 'a'),
(359, 'critical', 'If an authority figure makes a claim, does that automatically make it true?', 'Yes', 'No', '', '', 'b'),
(360, 'critical', 'Should assumptions always be made explicit in reasoning?', 'Yes', 'No', '', '', 'a\"'),
(361, 'critical', 'Can an argument be valid even if its conclusion is false?', 'Yes', 'No', '', '', 'a'),
(362, 'critical', 'If the premises are true and the reasoning is valid, must the conclusion be true?', 'Yes', 'No', '', '', 'a'),
(363, 'critical', 'Does the number of people who agree with an argument determine its validity?', 'Yes', 'No', '', '', 'b'),
(364, 'critical', 'If an argument uses vague terms, should it be questioned?', 'Yes', 'No', '', '', 'a'),
(365, 'critical', 'Can strong emotions interfere with logical reasoning?', 'Yes', 'No', '', '', 'a'),
(366, 'critical', 'If evidence is incomplete, should firm conclusions be avoided?', 'Yes', 'No', '', '', 'a'),
(367, 'critical', 'Does the order in which information is presented affect reasoning?', 'Yes', 'No', '', '', 'a'),
(368, 'critical', 'Should generalizations always be checked against specific evidence?', 'Yes', 'No', '', '', 'a'),
(369, 'critical', 'If two experts disagree, does it mean neither can be right?', 'Yes', 'No', '', '', 'b'),
(370, 'critical', 'Can an argument be relevant but still weak?', 'Yes', 'No', '', '', 'a\"'),
(371, 'critical', 'If reasoning is circular, is the argument flawed?', 'Yes', 'No', '', '', 'a'),
(372, 'critical', 'Should counterarguments always be considered in reasoning?', 'Yes', 'No', '', '', 'a'),
(373, 'critical', 'If evidence is biased, can the conclusion still be trusted?', 'Yes', 'No', '', '', 'b'),
(386, 'verbal', 'Fill in the blank: “He is very good ___ mathematics.”', 'A. at', 'B. in', 'C. on', 'D. with', 'a'),
(387, 'verbal', 'Which of these words is misspelled?', 'A. Accomodation', 'B. Accommodation', 'C. Occurrence', 'D. Beginning', 'a'),
(388, 'verbal', 'Choose the correct word: The movie was so ___ that everyone laughed.', 'A. humerous', 'B. humorous', 'C. humourus', 'D. humurous', 'b'),
(389, 'verbal', 'Identify the correctly punctuated sentence:', 'A. Its raining heavily.', 'B. It’s raining heavily.', 'C. Its’ raining heavily.', 'D. It rains heavily.', 'b'),
(390, 'verbal', 'Which is the synonym of \"ancient\"?', 'A. Old', 'B. Modern', 'C. Future', 'D. Recent', 'a'),
(391, 'verbal', 'Which phrase completes the sentence? “She is confident ___ her success.”', 'A. in', 'B. on', 'C. at', 'D. with', 'a'),
(392, 'verbal', 'Rearrange: \'the / market / to / went / she\' ', 'A. She went to market the', 'B. She went the market to', 'C. She went to the market', 'D. Went she to the market', 'c'),
(393, 'verbal', 'Find the odd one out:', 'A. Chair', 'B. Table', 'C. Cupboard', 'D. Chalk', 'd'),
(394, 'verbal', 'Which is a synonym of \"fragile\"?', 'A. Strong', 'B. Weak', 'C. Delicate', 'D. Hard', 'c'),
(395, 'verbal', 'Choose the opposite of \"optimistic\".', 'A. Cheerful', 'B. Hopeful', 'C. Pessimistic', 'D. Positive', 'c'),
(396, 'verbal', 'Choose the correct article: “He is ___ honest man.”', 'A. a', 'B. an', 'C. the', 'D. none', 'b'),
(397, 'verbal', 'Which word best completes the sentence? “She spoke so softly that I could ___ hear her.”', 'A. hardly', 'B. nearly', 'C. clearly', 'D. easily', 'a'),
(398, 'verbal', 'Pick the correctly spelled word:', 'A. Definately', 'B. Definitely', 'C. Definitly', 'D. Defenitely', 'b'),
(399, 'verbal', 'Choose the word that is most similar to \"rapid\".', 'A. Fast', 'B. Slow', 'C. Weak', 'D. Late', 'a'),
(400, 'verbal', 'Which of these is a one-word substitute for \"one who travels\"? ', 'A. Tourist', 'B. Passenger', 'C. Traveller', 'D. Voyager', 'c'),
(401, 'verbal', 'Select the best conclusion: “All dogs are mammals. Tommy is a dog.”', 'A. Tommy is a mammal.', 'B. Tommy is not a mammal.', 'C. Tommy may be a mammal.', 'D. Tommy dislikes mammals.', 'a'),
(402, 'verbal', 'Fill in the blank: \'Neither of the boys ___ present today.\'', 'A. are', 'B. were', 'C. is', 'D. have', 'c'),
(403, 'verbal', 'Choose the word opposite in meaning to \"bravery\".', 'A. Strength', 'B. Courage', 'C. Fear', 'D. Boldness', 'c'),
(404, 'verbal', 'Choose the synonym of \"generous\".', 'A. Mean', 'B. Kind', 'C. Selfish', 'D. Greedy', 'b'),
(417, 'logical', 'Find the missing number: 7, 14, 21, ?, 35', 'A. 25', 'B. 28', 'C. 30', 'D. 32', 'b'),
(418, 'logical', 'If all squares are rectangles, and all rectangles are shapes, then all squares are?', 'A. Shapes', 'B. Circles', 'C. Lines', 'D. Triangles', 'a'),
(419, 'logical', 'Which comes next in the pattern: AB, BC, CD, DE, ?', 'A. EF', 'B. FG', 'C. DF', 'D. GH', 'a'),
(420, 'logical', 'If SOME = 58, then NONE = ?', 'A. 56', 'B. 57', 'C. 58', 'D. 59', 'a'),
(421, 'logical', 'Which one does not belong? 2, 4, 8, 10, 16', 'A. 2', 'B. 4', 'C. 8', 'D. 10', 'd'),
(422, 'logical', 'John is taller than Peter. Peter is taller than Sam. Who is the tallest?', 'A. John', 'B. Peter', 'C. Sam', 'D. Cannot say', 'a'),
(423, 'logical', 'If in a code CAT = DBU, then DOG = ?', 'A. DPH', 'B. EPH', 'C. DPG', 'D. EOG', 'b'),
(424, 'logical', 'Find the missing term: 2, 6, 12, 20, ?', 'A. 28', 'B. 30', 'C. 32', 'D. 34', 'a'),
(425, 'logical', 'Choose the correct analogy: Eye : See :: Ear : ?', 'A. Sound', 'B. Listen', 'C. Hear', 'D. Noise', 'c'),
(426, 'logical', 'Which figure is the odd one out? Triangle, Square, Pentagon, Circle', 'A. Triangle', 'B. Square', 'C. Pentagon', 'D. Circle', 'd'),
(427, 'logical', 'If all books are pages and some pages are covers, what can we conclude?', 'A. Some books are covers', 'B. All covers are books', 'C. Some pages may be covers', 'D. Cannot say', 'c'),
(428, 'logical', 'Which number continues the series: 3, 6, 11, 18, ?', 'A. 25', 'B. 26', 'C. 27', 'D. 28', 'b'),
(429, 'logical', 'Find the odd one out: Paris, London, Rome, Amazon', 'A. Paris', 'B. London', 'C. Rome', 'D. Amazon', 'd'),
(430, 'logical', 'If TRAIN is coded as RTANI, then PLANE is coded as?', 'A. LPAEN', 'B. PALNE', 'C. ALPEN', 'D. PLEAN', 'b'),
(431, 'logical', 'Which number replaces the question mark? 1, 1, 2, 3, 5, 8, ?', 'A. 11', 'B. 12', 'C. 13', 'D. 14', 'c'),
(432, 'logical', 'If some pens are blue and all blue things are nice, what can be concluded?', 'A. Some pens are nice', 'B. All pens are nice', 'C. No pen is nice', 'D. Cannot say', 'a'),
(433, 'logical', 'Arrange the words logically: 1. Infant 2. Adult 3. Teenager 4. Old age', 'A. 1,3,2,4', 'B. 2,1,3,4', 'C. 3,1,2,4', 'D. 1,2,3,4', 'a'),
(434, 'logical', 'If all apples are fruits and some fruits are bananas, what can we conclude?', 'A. Some apples are bananas', 'B. All bananas are fruits', 'C. All fruits are apples', 'D. Cannot say', 'b'),
(435, 'logical', 'Which number continues the pattern: 4, 9, 16, 25, ?', 'A. 30', 'B. 34', 'C. 36', 'D. 40', 'c'),
(448, 'numerical', 'If 12 men can complete a task in 15 days, how many men are needed to complete it in 10 days?', '12', '15', '18', '20', 'c'),
(449, 'numerical', 'Simplify: (3/4) ÷ (9/16)', '2/3', '4/3', '16/27', '27/16', 'b'),
(450, 'numerical', 'The perimeter of a square is 64 cm. What is its area?', '128', '196', '256', '512', 'c'),
(451, 'numerical', 'If the cost price is MWK240 and the selling price is MWK300, what is the profit percentage?', '20%', '22%', '25%', '30%', 'c'),
(452, 'numerical', 'What is 15% of 480?', '60', '62', '68', '72', 'd'),
(453, 'numerical', 'Solve for x: 2x + 5 = 19', '6', '7', '8', '9', 'b'),
(454, 'numerical', 'The LCM of 12 and 18 is?', '24', '30', '36', '48', 'c'),
(455, 'numerical', 'A sum of money doubles in 12 years at simple interest. What is the rate per annum?', '6%', '8%', '10%', '12%', 'b'),
(456, 'numerical', 'The difference between the squares of 15 and 13 is?', '28', '54', '56', '60', 'c'),
(457, 'numerical', 'If the speed of a car is 72 km/h, how many meters does it travel per second?', '15', '18', '20', '25', 'b'),
(458, 'numerical', 'What is the simple interest on MWK1200 at 10% per annum for 2 years?', '120', '200', '240', '300', 'c'),
(459, 'numerical', 'If 20% of a number is 50, what is the number?', '200', '210', '220', '250', 'a'),
(460, 'numerical', 'The cost of 12 pens is MWK180. What is the cost of 20 pens?', 'MWK280', 'MWK290', 'MWK300', 'MWK320', 'c'),
(461, 'numerical', 'What is the probability of getting an odd number when a dice is rolled?', '1/2', '1/3', '2/3', '5/6', 'a'),
(462, 'numerical', 'A train travels 180 km in 3 hours. What is its speed?', '40', '50', '60', '70', 'c'),
(463, 'numerical', 'The average of 5 consecutive odd numbers is 25. What is the largest number?', '29', '31', '33', '35', 'b'),
(464, 'numerical', 'The sum of the first 10 natural numbers is?', '45', '50', '55', '60', 'b'),
(465, 'numerical', 'If a = 5, b = 3, find the value of a² + b²', '25', '34', '35', '38', 'b'),
(466, 'numerical', 'A man bought a shirt for MWK500 and sold it at a loss of 10%. What is the selling price?', 'MWK450', 'MWK460', 'MWK470', 'MWK480', 'a');

-- --------------------------------------------------------

--
-- Table structure for table `schemes`
--

CREATE TABLE `schemes` (
  `id` int(11) NOT NULL,
  `scheme_name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `eligibility_criteria` text DEFAULT NULL,
  `benefit_details` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `schemes`
--

INSERT INTO `schemes` (`id`, `scheme_name`, `description`, `eligibility_criteria`, `benefit_details`) VALUES
(1, 'Merit-Based Scheme', 'Awards students for outstanding academic performance.', 'Must maintain a GPA of 3.8 or higher and be enrolled full-time.', 'Full tuition waiver and academic materials support.'),
(2, 'Need-Based Scheme', 'Supports students from low-income families.', 'Household income must be below the university’s defined threshold and proof of financial hardship required.', 'Covers 50% of tuition and provides meal allowances.'),
(3, 'STEM Scheme', 'Encourages students pursuing science, technology, engineering, and mathematics fields.', 'Must be enrolled in a STEM program with a GPA of at least 3.5.', 'Tuition coverage and annual equipment or lab allowance.'),
(4, 'Sports Scholarship Scheme', 'Rewards talented student athletes who represent the university.', 'Must participate in official university sports and maintain a GPA above 2.8.', 'Partial tuition waiver and access to sports facilities.'),
(5, 'Community Service Scheme', 'Recognizes students engaged in meaningful volunteer work.', 'Must complete at least 100 hours of verified community service.', 'Tuition discount and certificate of recognition.'),
(6, 'Research and Innovation Scheme', 'Promotes creativity and innovation through research projects.', 'Must submit a research proposal approved by the academic board.', 'Funding for project materials and publication support.'),
(7, 'Disability Support Scheme', 'Assists students with physical or learning disabilities.', 'Must provide official medical documentation of disability.', 'Full tuition waiver and assistive learning resources.'),
(8, 'Female Empowerment Scheme', 'Encourages female students to pursue higher education.', 'Must be a female student demonstrating academic potential or leadership.', 'Partial or full tuition support and mentorship opportunities.'),
(9, 'Alumni-Funded Scheme', 'Funded by university alumni to support deserving students.', 'Open to all students who demonstrate commitment to academic excellence.', 'Variable funding covering tuition or living expenses.'),
(10, 'International Student Scheme', 'Designed for students from other countries studying at the university.', 'Must hold a valid student visa and demonstrate strong academic records.', 'Covers a percentage of tuition and accommodation fees.'),
(11, 'Cultural or Arts Scheme', 'Supports students talented in performing or visual arts.', 'Must provide a portfolio or proof of participation in arts-related activities.', 'Tuition support and funding for materials or exhibitions.'),
(12, 'Leadership Development Scheme', 'Recognizes students who exhibit strong leadership and community engagement.', 'Must hold or have held a leadership position within the university or community.', 'Scholarship plus access to leadership training programs.'),
(13, 'Rural or Underprivileged Scheme', 'Helps students from rural or economically disadvantaged backgrounds.', 'Must provide proof of residence in a designated rural area or financial need.', 'Full or partial tuition coverage and travel allowance.'),
(14, 'Partner Organization Scheme', 'Available through partnerships with external organizations.', 'Must meet the specific criteria set by the partnering organization.', 'Funding level varies based on partnership terms.'),
(15, 'Government-Funded Scheme', 'Supported by government initiatives to promote education.', 'Must meet government-specified eligibility and performance standards.', 'Covers tuition and provides a living stipend.');

-- --------------------------------------------------------

--
-- Table structure for table `scholarships`
--

CREATE TABLE `scholarships` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `scheme_type` varchar(100) DEFAULT NULL,
  `file_path` varchar(255) NOT NULL,
  `admin_id` int(11) NOT NULL,
  `deadline` date DEFAULT curdate(),
  `descrip` varchar(150) DEFAULT 'No Description',
  `provider` varchar(150) DEFAULT NULL,
  `financial_amount` varchar(20) DEFAULT NULL,
  `applicantion_link` varchar(255) DEFAULT NULL,
  `provider_email` varchar(150) DEFAULT NULL,
  `subject` varchar(50) DEFAULT NULL,
  `scheme_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `scholarships`
--

INSERT INTO `scholarships` (`id`, `name`, `scheme_type`, `file_path`, `admin_id`, `deadline`, `descrip`, `provider`, `financial_amount`, `applicantion_link`, `provider_email`, `subject`, `scheme_id`) VALUES
(12, 'ewrubvwierb', 'Government', '1756145025_0 Backend Development .pdf', 15, '2025-10-01', 'qwrifubqiwufjq', 'kjewbrkjber', 'Partial', 'ekrjbwkejrfbkq', 'qwkejfqwkjf', 'Computer Science & IT', NULL),
(13, 'wqlfblkwjb', 'Agriculture/Environment', '1756147159_ITDSABD Topic 3 Understanding Data  Exploration.pdf', 15, '2025-10-01', 'kqwejfkqwjlbf', 'khjwflkjee', 'Lump Sum', 'kwjqnlfjne', 'qwkjbeflkj', 'Arts & Humanities', NULL),
(17, 'qwkjfbkqer', 'Agriculture/Environment', '1756150845_studentGuideOld.pdf', 15, '2025-10-01', 'qkwjfblw', 'erngrgk', 'Partial', 'kejwrbfkwej', 'kqwjbfkqj', 'Dentistry', NULL),
(18, 'qwkejfnkwj', 'Agriculture/Environment', '1756151005_ITDSABD Topic 2 Introduction to Data.pdf', 15, '2025-10-01', 'qwkjebfjw', 'wkefbqwkef', 'Partial', 'walkjfqbwelkrjf', 'qkwjrfblkqerbf', 'Law', NULL),
(19, 'NCC scholar', 'Business/Entrepreneurship', '1759518981_ITDSABD Topic 11 Data Science Ethics.pdf', 15, '2025-09-30', 'extend your education studies', 'NCC', 'Stipend', 'www.Ncc.ca.za', 'ncc@gmail.com', 'Communications & Media Studies', NULL),
(20, 'Dom clean scholar', 'Female Empowerment Scheme', '1760438731_mySignature.pdf', 15, '2025-12-04', 'For the ladies', 'dom clean lim', 'Stipend', 'www.dom.co.za', 'domClean@gmail.com', '', 8);

-- --------------------------------------------------------

--
-- Table structure for table `sholarship_perks`
--

CREATE TABLE `sholarship_perks` (
  `scholarship_id` int(11) NOT NULL,
  `perk_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sholarship_perks`
--

INSERT INTO `sholarship_perks` (`scholarship_id`, `perk_id`) VALUES
(17, 2),
(17, 3),
(18, 2),
(18, 3),
(18, 4),
(18, 5),
(18, 6),
(19, 2),
(19, 4),
(20, 2),
(20, 4),
(20, 6);

-- --------------------------------------------------------

--
-- Table structure for table `weights`
--

CREATE TABLE `weights` (
  `id` int(11) NOT NULL,
  `academic` float DEFAULT NULL,
  `assessment` float DEFAULT NULL,
  `financial` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `weights`
--

INSERT INTO `weights` (`id`, `academic`, `assessment`, `financial`) VALUES
(1, 5, 4, 3.5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `applicant`
--
ALTER TABLE `applicant`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `reviewer_id` (`reviewer_id`);

--
-- Indexes for table `applications`
--
ALTER TABLE `applications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `scholarship_id` (`scholarship_id`);

--
-- Indexes for table `assessment`
--
ALTER TABLE `assessment`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `documents`
--
ALTER TABLE `documents`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `foreign_key_applications` (`application_ID`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sender_id` (`sender_id`);

--
-- Indexes for table `perks`
--
ALTER TABLE `perks`
  ADD PRIMARY KEY (`perk_id`);

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `schemes`
--
ALTER TABLE `schemes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `scholarships`
--
ALTER TABLE `scholarships`
  ADD PRIMARY KEY (`id`),
  ADD KEY `admin_id` (`admin_id`),
  ADD KEY `foreign_key_schemeID` (`scheme_id`);

--
-- Indexes for table `sholarship_perks`
--
ALTER TABLE `sholarship_perks`
  ADD PRIMARY KEY (`scholarship_id`,`perk_id`),
  ADD KEY `perk_id` (`perk_id`);

--
-- Indexes for table `weights`
--
ALTER TABLE `weights`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `applicant`
--
ALTER TABLE `applicant`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `applications`
--
ALTER TABLE `applications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `assessment`
--
ALTER TABLE `assessment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `documents`
--
ALTER TABLE `documents`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `perks`
--
ALTER TABLE `perks`
  MODIFY `perk_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=467;

--
-- AUTO_INCREMENT for table `schemes`
--
ALTER TABLE `schemes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `scholarships`
--
ALTER TABLE `scholarships`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `weights`
--
ALTER TABLE `weights`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `applicant`
--
ALTER TABLE `applicant`
  ADD CONSTRAINT `applicant_ibfk_1` FOREIGN KEY (`reviewer_id`) REFERENCES `admin` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `applications`
--
ALTER TABLE `applications`
  ADD CONSTRAINT `applications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `applicant` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `applications_ibfk_2` FOREIGN KEY (`scholarship_id`) REFERENCES `scholarships` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `documents`
--
ALTER TABLE `documents`
  ADD CONSTRAINT `documents_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `applicant` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `documents_ibfk_2` FOREIGN KEY (`application_ID`) REFERENCES `applications` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `admin` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `scholarships`
--
ALTER TABLE `scholarships`
  ADD CONSTRAINT `scholarships_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `scholarships_ibfk_2` FOREIGN KEY (`scheme_id`) REFERENCES `schemes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `sholarship_perks`
--
ALTER TABLE `sholarship_perks`
  ADD CONSTRAINT `sholarship_perks_ibfk_1` FOREIGN KEY (`scholarship_id`) REFERENCES `scholarships` (`id`),
  ADD CONSTRAINT `sholarship_perks_ibfk_2` FOREIGN KEY (`perk_id`) REFERENCES `perks` (`perk_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
