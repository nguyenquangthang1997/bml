-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Máy chủ: localhost:3306
-- Thời gian đã tạo: Th10 29, 2019 lúc 05:24 PM
-- Phiên bản máy phục vụ: 5.7.28-0ubuntu0.18.04.4
-- Phiên bản PHP: 7.2.24-0ubuntu0.18.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `test`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `action`
--

CREATE TABLE `action` (
  `id` int(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `time` int(255) NOT NULL,
  `user_id` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Đang đổ dữ liệu cho bảng `action`
--

INSERT INTO `action` (`id`, `description`, `time`, `user_id`) VALUES
(1, 'tuoi cay', 63, 1),
(2, 'tuoi phan', 28, 1),
(3, 'cat tia', 92, 4),
(4, 'tuoi cay', 95, 2),
(5, 'cat tia', 85, 5),
(6, 'tuoi phan', 34, 1),
(7, 'cat tia', 84, 3),
(8, 'tuoi phan', 53, 9),
(9, 'cat tia', 80, 2),
(10, 'thu hoach', 65, 10);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `land`
--

CREATE TABLE `land` (
  `id` int(255) NOT NULL,
  `square` int(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `user_id` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Đang đổ dữ liệu cho bảng `land`
--

INSERT INTO `land` (`id`, `square`, `address`, `user_id`) VALUES
(1, 63, 'david', 1),
(2, 28, 'rogers', 2),
(3, 92, 'david', 3),
(4, 95, 'maria', 5),
(5, 85, 'morris', 4),
(6, 34, 'daniel', 7),
(7, 84, 'sanders', 8),
(8, 53, 'mark', 9),
(9, 80, 'morgan', 6),
(10, 65, 'paul', 10);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `product`
--

CREATE TABLE `product` (
  `id` int(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `user_id` int(255) NOT NULL,
  `land_id` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Đang đổ dữ liệu cho bảng `product`
--

INSERT INTO `product` (`id`, `name`, `user_id`, `land_id`) VALUES
(1, 'dao', 2, 1),
(2, 'tao', 2, 3),
(3, 'man', 2, 5),
(4, 'ngo', 2, 5),
(5, 'ca chua', 6, 8),
(6, 'oi', 6, 4),
(7, 'trung', 6, 4),
(8, 'thit', 6, 3),
(9, 'ca', 6, 8),
(10, 'nhan', 6, 1);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `user`
--

CREATE TABLE `user` (
  `id` int(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `password` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Đang đổ dữ liệu cho bảng `user`
--

INSERT INTO `user` (`id`, `name`, `type`, `password`) VALUES
(1, 'rogers63', 'nd', 1),
(2, 'mike28', 'dg', 1),
(3, 'rivera92', 'vc', 1),
(4, 'ross95', 'vc', 1),
(5, 'paul85', 'boss', 1),
(6, 'smith34', 'dg', 1),
(7, 'james84', 'nd', 1),
(8, 'daniel53', 'vc', 1),
(9, 'brooks80', 'vc', 1),
(10, 'morgan65', 'vc', 1);

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `action`
--
ALTER TABLE `action`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `land`
--
ALTER TABLE `land`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `action`
--
ALTER TABLE `action`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT cho bảng `land`
--
ALTER TABLE `land`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT cho bảng `product`
--
ALTER TABLE `product`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT cho bảng `user`
--
ALTER TABLE `user`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
