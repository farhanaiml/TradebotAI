-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 30, 2023 at 07:13 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `1stocknew`
--

-- --------------------------------------------------------

--
-- Table structure for table `chattb`
--

CREATE TABLE `chattb` (
  `Id` bigint(20) NOT NULL auto_increment,
  `ExpertName` varchar(250) NOT NULL,
  `Query` varchar(500) NOT NULL,
  `Answer` varchar(500) NOT NULL,
  `Date` varchar(250) NOT NULL,
  PRIMARY KEY  (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `chattb`
--

INSERT INTO `chattb` (`Id`, `ExpertName`, `Query`, `Answer`, `Date`) VALUES
(1, 'sangeeth', 'Apple', 'Apple Stock 42', '26-Apr-2023'),
(2, 'san', 'today google stock', '455', '30-Apr-2023');

-- --------------------------------------------------------

--
-- Table structure for table `experttb`
--

CREATE TABLE `experttb` (
  `id` bigint(10) NOT NULL auto_increment,
  `Name` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `experttb`
--

INSERT INTO `experttb` (`id`, `Name`, `Mobile`, `Email`, `UserName`, `Password`) VALUES
(1, 'sangeeth Kumar', 'sangeeth5535@gmail.com', '9486365535', 'sangeeth', 'sangeeth'),
(2, 'sangeeth Kumar', 'sangeeth5535@gmail.com', '9486365535', 'san', 'san'),
(3, 'sri', 'sri@gmail.com', '9486365535', 'sri', 'sri');

-- --------------------------------------------------------

--
-- Table structure for table `querytb`
--

CREATE TABLE `querytb` (
  `id` bigint(10) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  `Query` varchar(500) NOT NULL,
  `Answer` varchar(1000) NOT NULL,
  `ExpertName` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `querytb`
--

INSERT INTO `querytb` (`id`, `UserName`, `Query`, `Answer`, `ExpertName`) VALUES
(1, 'san', 'best invesment', 'yahoo', 'sangeeth'),
(2, 'sri', 'today tra', 'google', 'san');

-- --------------------------------------------------------

--
-- Table structure for table `regtb`
--

CREATE TABLE `regtb` (
  `id` bigint(10) NOT NULL auto_increment,
  `Name` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `regtb`
--

INSERT INTO `regtb` (`id`, `Name`, `Mobile`, `Email`, `UserName`, `Password`) VALUES
(1, 'sangeeth Kumar', 'sangeeth5535@gmail.com', '9486365535', 'san', 'san'),
(2, 'sri', 'sangeeth5535@gmail.com', '9486365535', 'sri', 'sri');

-- --------------------------------------------------------

--
-- Table structure for table `stocktb`
--

CREATE TABLE `stocktb` (
  `Id` bigint(10) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  `StockName` varchar(250) NOT NULL,
  `date` date NOT NULL,
  `coun` int(10) NOT NULL,
  PRIMARY KEY  (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `stocktb`
--

INSERT INTO `stocktb` (`Id`, `UserName`, `StockName`, `date`, `coun`) VALUES
(1, 'san', 'AAPL', '0000-00-00', 1),
(2, 'san', 'GE', '2023-04-26', 1),
(3, 'sri', 'AAPL', '2023-04-30', 1),
(4, 'san', 'TCS', '2023-04-30', 1);
