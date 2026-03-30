-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th3 30, 2026 lúc 01:41 PM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `hospital_db`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `doctors`
--

CREATE TABLE `doctors` (
  `Doctor_id` int(11) NOT NULL,
  `Full_name` varchar(255) NOT NULL,
  `Specialization` varchar(255) NOT NULL,
  `Account` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Phone` varchar(20) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `doctors`
--

INSERT INTO `doctors` (`Doctor_id`, `Full_name`, `Specialization`, `Account`, `Password`, `Phone`, `created_at`) VALUES
(1, 'BS. Đặng Minh Tân', 'Chuyên gia Hệ thống', 'tan_admin', '123', '0901234567', '2026-03-30 18:33:05'),
(2, 'BS. Vũ Thanh Tùng', 'Nội khoa', 'tung_bs', '123', '0907654321', '2026-03-30 18:33:05'),
(3, 'BS. Trần Văn Trung', 'Nhi khoa', 'trung_bs', '123', '0909998887', '2026-03-30 18:33:05');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `medicalrecords`
--

CREATE TABLE `medicalrecords` (
  `Record_id` int(11) NOT NULL,
  `Patient_id` int(11) NOT NULL,
  `Doctor_id` int(11) NOT NULL,
  `Visit_date` date DEFAULT NULL,
  `Symptoms` text DEFAULT NULL,
  `Diagnosis` text DEFAULT NULL,
  `Treatment` text DEFAULT NULL,
  `Notes` text DEFAULT NULL,
  `Status` varchar(50) DEFAULT 'Chờ khám',
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `medicalrecords`
--

INSERT INTO `medicalrecords` (`Record_id`, `Patient_id`, `Doctor_id`, `Visit_date`, `Symptoms`, `Diagnosis`, `Treatment`, `Notes`, `Status`, `created_at`) VALUES
(1, 1, 1, '2026-03-30', 'đau nửa đầu', 'tụ máu não', 'phẫu thuật', NULL, 'Đã khám', '2026-03-30 18:33:05'),
(2, 3, 1, '2026-03-30', 'Đau bụng âm ỉ', NULL, NULL, NULL, 'Chờ khám', '2026-03-30 18:33:05'),
(3, 5, 1, '2026-03-30', 'Nhức đầu kéo dài', NULL, NULL, NULL, 'Chờ khám', '2026-03-30 18:33:05'),
(4, 7, 2, '2026-03-30', 'Ho khan, tức ngực', NULL, NULL, NULL, 'Chờ khám', '2026-03-30 18:33:05'),
(5, 2, 1, '2026-03-30', 'Đau tai', 'Viêm tai giữa', 'Nhỏ thuốc Otrivin 2 lần/ngày', NULL, 'Đã khám', '2026-03-30 18:33:05'),
(6, 4, 3, '2026-03-30', 'Phát ban', 'Dị ứng thời tiết', 'Uống thuốc kháng Histamine', NULL, 'Đã khám', '2026-03-30 18:33:05'),
(7, 6, 1, '2026-03-31', 'Tái khám định kỳ', NULL, NULL, NULL, 'Chờ khám', '2026-03-30 18:33:05'),
(8, 8, 2, '2026-04-01', 'Kiểm tra sức khỏe tổng quát', NULL, NULL, NULL, 'Chờ khám', '2026-03-30 18:33:05'),
(9, 10, 1, '2026-04-06', 'Theo dõi huyết áp', NULL, NULL, NULL, 'Chờ khám', '2026-03-30 18:33:05'),
(10, 1, 1, '2026-03-01', 'Cảm cúm nhẹ', 'Cảm lạnh', 'Nghỉ ngơi, uống nhiều nước', NULL, 'Đã khám', '2026-03-30 18:33:05');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `patients`
--

CREATE TABLE `patients` (
  `Patient_id` int(11) NOT NULL,
  `Full_name` varchar(255) NOT NULL,
  `Dob` date DEFAULT NULL,
  `Gender` varchar(10) NOT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  `Address` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `patients`
--

INSERT INTO `patients` (`Patient_id`, `Full_name`, `Dob`, `Gender`, `Phone`, `Address`, `created_at`) VALUES
(1, 'Nguyễn Văn An', '1995-05-20', 'Nam', '0911000111', 'Hà Nội', '2026-03-30 18:33:05'),
(2, 'Trần Thị Bình', '1988-10-12', 'Nữ', '0911000222', 'Hải Phòng', '2026-03-30 18:33:05'),
(3, 'Lê Văn Cường', '2000-01-15', 'Nam', '0911000333', 'Đà Nẵng', '2026-03-30 18:33:05'),
(4, 'Phạm Minh Đức', '1992-03-30', 'Nam', '0911000444', 'TP.HCM', '2026-03-30 18:33:05'),
(5, 'Hoàng Bảo Yến', '2005-07-08', 'Nữ', '0911000555', 'Cần Thơ', '2026-03-30 18:33:05'),
(6, 'Đỗ Hùng Dũng', '1990-12-25', 'Nam', '0911000666', 'Gia Lai', '2026-03-30 18:33:05'),
(7, 'Bùi Tiến Dũng', '1997-02-28', 'Nam', '0911000777', 'Thanh Hóa', '2026-03-30 18:33:05'),
(8, 'Nguyễn Quang Hải', '1997-04-12', 'Nam', '0911000888', 'Đông Anh', '2026-03-30 18:33:05'),
(9, 'Đoàn Văn Hậu', '1999-04-19', 'Nam', '0911000999', 'Thái Bình', '2026-03-30 18:33:05'),
(10, 'Nguyễn Công Phượng', '1995-01-21', 'Nam', '0911000000', 'Nghệ An', '2026-03-30 18:33:05');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `doctors`
--
ALTER TABLE `doctors`
  ADD PRIMARY KEY (`Doctor_id`),
  ADD UNIQUE KEY `Account` (`Account`);

--
-- Chỉ mục cho bảng `medicalrecords`
--
ALTER TABLE `medicalrecords`
  ADD PRIMARY KEY (`Record_id`),
  ADD KEY `FK_Patient` (`Patient_id`),
  ADD KEY `FK_Doctor` (`Doctor_id`);

--
-- Chỉ mục cho bảng `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`Patient_id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `doctors`
--
ALTER TABLE `doctors`
  MODIFY `Doctor_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT cho bảng `medicalrecords`
--
ALTER TABLE `medicalrecords`
  MODIFY `Record_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT cho bảng `patients`
--
ALTER TABLE `patients`
  MODIFY `Patient_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `medicalrecords`
--
ALTER TABLE `medicalrecords`
  ADD CONSTRAINT `FK_Doctor` FOREIGN KEY (`Doctor_id`) REFERENCES `doctors` (`Doctor_id`),
  ADD CONSTRAINT `FK_Patient` FOREIGN KEY (`Patient_id`) REFERENCES `patients` (`Patient_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
