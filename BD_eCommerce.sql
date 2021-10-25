-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 24, 2021 at 11:53 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `inventario_mazda`
--

-- --------------------------------------------------------

--
-- Table structure for table `usuarios`
--

CREATE TABLE `usuarios` (
  `codigo` int(11) NOT NULL,
  `nombre` varchar(250) NOT NULL,
  `apellidos` varchar(250) NOT NULL,
  `email` varchar(250) NOT NULL,
  `rol` varchar(250) NOT NULL,
  `contraseña` varchar(250) NOT NULL,
  `created` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `usuarios`
--

INSERT INTO `usuarios` (`codigo`, `nombre`, `apellidos`, `email`, `rol`, `contraseña`, `created`) VALUES
(1, 'LUIS CARLOS', 'HERRERA FERRER', 'LUYSHERRERAF@GMAIL.COM', 'FINALUSER', '$2b$12$zmo6qzn8bySg6cNzg7Hz8u5M.2T1RxFB5Pcb5U7SJ2gMbrIObWVBK', '0000-00-00 00:00:00'),
(2, 'MARITZA LORENA', 'REY JOSEFINA', 'LORE@GMAIL.COM', 'FINALUSER', '$2b$12$zmo6qzn8bySg6cNzg7Hz8unwUBpQthrlPGTxDW5TxU//.mLyAzVFO', '0000-00-00 00:00:00'),
(3, 'LUIS CARLOS', 'HERRERA FERRER', 'LUIS@GMAIL.COM', 'FINALUSER', '$2b$12$c8nahIcG5b6fiiZ/qRt6L.qtK6iVzD1xXlsBP4EsM6fgepsk7NfC.', '0000-00-00 00:00:00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`codigo`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `codigo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
