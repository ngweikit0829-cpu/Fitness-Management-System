-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Sep 28, 2026 at 08:13 AM
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
-- Database: `fitness_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `exercises`
--

CREATE TABLE `exercises` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `muscle_group` varchar(20) NOT NULL,
  `category` varchar(20) NOT NULL DEFAULT 'strength',
  `description` text DEFAULT NULL,
  `default_sets_reps` varchar(20) DEFAULT NULL
) ;

--
-- Dumping data for table `exercises`
--

INSERT INTO `exercises` (`id`, `name`, `muscle_group`, `category`, `description`, `default_sets_reps`) VALUES
(1, '杠铃卧推', '胸部', 'strength', '平躺推起杠铃至手臂伸直，缓慢下放至胸口上方', '4x10'),
(2, '哑铃飞鸟', '胸部', 'strength', '双手持哑铃，手肘微屈，弧线打开至与肩齐平后收拢', '3x12'),
(3, '引体向上', '背部', 'strength', '双手宽握吊杆，收紧背部将身体拉至下巴过杠', '4x8'),
(4, '杠铃划船', '背部', 'strength', '上身前倾，收紧核心，将杠铃拉向腹部再缓慢放下', '4x10'),
(5, '杠铃深蹲', '腿部', 'strength', '杠铃置于斜方肌，屈膝下蹲至大腿与地面平行', '4x12'),
(6, '保加利亚分腿蹲', '腿部', 'strength', '后脚置于凳上，前腿屈膝下蹲，保持躯干直立', '3x10'),
(7, '哑铃肩上推举', '肩部', 'strength', '双手持哑铃于肩侧，向上推起至手臂伸直', '3x12'),
(8, '侧平举', '肩部', 'strength', '双手持哑铃于体侧，缓慢平举至与肩齐平', '3x15'),
(9, '杠铃弯举', '手臂', 'strength', '手肘固定，弯举杠铃至肱二头肌顶峰收缩', '3x12'),
(10, '绳索下压', '手臂', 'strength', '手肘贴紧身体，下压绳索至手臂完全伸直', '3x15'),
(11, '平板支撑', '核心', 'mobility', '前臂撑地，保持身体一条直线，收紧腹部', '3x45s'),
(12, '卷腹', '核心', 'strength', '仰卧屈膝，收缩腹肌将上背部抬离地面', '3x20'),
(13, '上斜哑铃推举', '胸部', 'strength', '仰卧斜板，控制哑铃下放后向上推起', '3x10'),
(14, '俯卧撑', '胸部', 'strength', '身体保持直线，屈肘下沉后推回起始位置', '3x12'),
(15, '单臂哑铃划船', '背部', 'strength', '支撑身体，收紧背部将哑铃拉向腰部', '3x10'),
(16, '高位下拉', '背部', 'strength', '保持躯干稳定，将横杆下拉至胸前', '3x12'),
(17, '罗马尼亚硬拉', '腿部', 'strength', '髋部后移，保持背部中立并用臀腿发力站起', '3x10'),
(18, '臀桥', '腿部', 'strength', '仰卧屈膝，收紧臀部将髋部抬起', '3x15'),
(19, '面拉', '肩部', 'strength', '将绳索拉向面部，保持肩胛骨稳定', '3x15'),
(20, '俯身反向飞鸟', '肩部', 'strength', '俯身抬起哑铃，感受后束三角肌收缩', '3x12'),
(21, '锤式弯举', '手臂', 'strength', '保持掌心相对，将哑铃弯举至肩部', '3x12'),
(22, '哑铃三头肌伸展', '手臂', 'strength', '双手持哑铃屈肘下放，再伸展手臂回到起始位置', '3x10'),
(23, '俄罗斯转体', '核心', 'strength', '坐姿收紧核心，躯干向两侧缓慢转动', '3x20'),
(24, '死虫式', '核心', 'mobility', '仰卧保持腰背贴地，交替伸展对侧手脚', '3x10');

-- --------------------------------------------------------

--
-- Table structure for table `fooditems`
--

CREATE TABLE `fooditems` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `meal_type` varchar(20) DEFAULT NULL,
  `calories` float NOT NULL,
  `protein` float NOT NULL DEFAULT 0,
  `carbs` float NOT NULL DEFAULT 0,
  `fat` float NOT NULL DEFAULT 0,
  `image_filename` varchar(255) DEFAULT NULL
) ;

--
-- Dumping data for table `fooditems`
--

INSERT INTO `fooditems` (`id`, `name`, `meal_type`, `calories`, `protein`, `carbs`, `fat`, `image_filename`) VALUES
(1, '鸡胸肉', 'any', 133, 24.6, 0, 3.6, 'Chicken Breast.jpg'),
(2, '糙米（熟）', 'any', 112, 2.6, 23.5, 0.9, 'Brown Rice.jpg'),
(3, '三文鱼', 'any', 208, 20.4, 0, 13.4, 'Salmon.jpg'),
(4, '燕麦片', 'breakfast', 389, 16.9, 66.3, 6.9, 'Oatmeal.webp'),
(5, '西兰花', 'any', 34, 2.8, 6.6, 0.4, 'Broccoli.jpg'),
(6, '鸡蛋', 'breakfast', 143, 12.6, 0.7, 9.5, 'Egg.webp'),
(7, '低脂牛奶', 'breakfast', 42, 3.4, 5, 1, 'low-fat-milk.webp'),
(8, '藜麦（熟）', 'dinner', 120, 4.4, 21.3, 1.9, 'quinoa.jpg'),
(9, '香蕉', 'breakfast', 89, 1.1, 22.8, 0.3, 'Banana.jpg'),
(10, '苹果', 'breakfast', 52, 0.3, 13.8, 0.2, 'Apple.jpg'),
(11, '地瓜（熟）', 'any', 90, 2, 20.7, 0.2, 'Cooked sweet potato.jpg'),
(12, '全麦面包', 'breakfast', 247, 13, 41.3, 4.2, 'Whole wheat bread.jpg'),
(13, '嫩豆腐', 'any', 76, 8.1, 1.9, 4.2, 'Soft tofu.jpg'),
(14, '金枪鱼（水浸）', 'any', 116, 25.5, 0, 0.8, 'Tuna canned in water.jpg'),
(15, '瘦牛肉（熟）', 'any', 217, 26.1, 0, 11.8, 'Cooked lean beef.jpg'),
(16, '菠菜', 'any', 23, 2.9, 3.6, 0.4, 'Spinach.jpg'),
(17, '鹰嘴豆（熟）', 'any', 164, 8.9, 27.4, 2.6, 'Cooked chickpeas.webp'),
(18, '牛油果', 'any', 160, 2, 8.5, 14.7, 'Avocado.webp'),
(19, '低脂茅屋奶酪', 'breakfast', 82, 11.1, 4.3, 2.3, 'Low-fat cottage cheese.jpg'),
(20, '希腊酸奶', 'breakfast', 59, 10.3, 3.6, 0.4, 'Greek yogurt.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `healthlogs`
--

CREATE TABLE `healthlogs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `log_date` date NOT NULL,
  `weight` float NOT NULL,
  `bmi` float NOT NULL,
  `water_intake` int(11) NOT NULL DEFAULT 0,
  `notes` text DEFAULT NULL
) ;

--
-- Dumping data for table `healthlogs`
--

INSERT INTO `healthlogs` (`id`, `user_id`, `log_date`, `weight`, `bmi`, `water_intake`, `notes`) VALUES
(8, 1, '2026-09-15', 72, 22.7, 0, '档案体重更新'),
(17, 1, '2026-09-23', 71.5, 22.6, 2000, '档案体重更新'),
(32, 1, '2026-09-22', 71, 22.4, 1950, ''),
(33, 1, '2026-09-27', 72, 22.7, 2300, '非常棒'),
(34, 1, '2026-09-26', 71, 22.4, 1800, '背部有感觉'),
(36, 2, '2026-09-27', 61, 23.8, 2000, '没有训练'),
(37, 2, '2026-09-28', 30, 11.7, 3000, 'normal'),
(38, 2, '2026-09-24', 50, 19.5, 1000, 'bad'),
(41, 2, '2026-09-18', 80, 31.2, 2000, '。。。。。。。。。。'),
(45, 2, '2026-09-04', 60, 23.4, 3000, 'okok');

-- --------------------------------------------------------

--
-- Table structure for table `reporthistory`
--

CREATE TABLE `reporthistory` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `days` int(11) NOT NULL,
  `generated_at` datetime NOT NULL DEFAULT current_timestamp()
) ;

--
-- Dumping data for table `reporthistory`
--

INSERT INTO `reporthistory` (`id`, `user_id`, `days`, `generated_at`) VALUES
(4, 1, 7, '2026-09-23 15:45:25'),
(5, 1, 7, '2026-09-28 12:32:20'),
(6, 2, 30, '2026-09-28 13:09:53'),
(7, 2, 30, '2026-09-28 13:14:07'),
(8, 2, 30, '2026-09-28 13:29:01'),
(9, 2, 30, '2026-09-28 13:29:07'),
(10, 2, 30, '2026-09-28 13:29:16'),
(11, 2, 30, '2026-09-28 13:29:26'),
(12, 2, 30, '2026-09-28 13:29:31'),
(13, 2, 30, '2026-09-28 13:29:39'),
(14, 2, 7, '2026-09-28 13:33:24'),
(15, 2, 7, '2026-09-28 13:33:33'),
(16, 2, 7, '2026-09-28 13:33:44'),
(17, 2, 7, '2026-09-28 13:42:39'),
(18, 2, 30, '2026-09-28 13:46:19'),
(19, 2, 7, '2026-09-28 13:47:21'),
(20, 2, 7, '2026-09-28 13:47:25'),
(21, 2, 30, '2026-09-28 13:47:35'),
(22, 2, 7, '2026-09-28 13:53:20'),
(23, 2, 30, '2026-09-28 13:53:35'),
(24, 1, 30, '2026-09-28 14:01:32'),
(25, 1, 30, '2026-09-28 14:06:09'),
(26, 1, 30, '2026-09-28 14:08:09'),
(27, 1, 30, '2026-09-28 14:09:03'),
(28, 1, 7, '2026-09-28 14:09:11'),
(29, 1, 30, '2026-09-28 14:09:18'),
(30, 1, 30, '2026-09-28 14:10:02'),
(31, 1, 7, '2026-09-28 14:11:46');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `age` int(11) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `height` float NOT NULL,
  `initial_weight` float NOT NULL,
  `activity_level` varchar(20) NOT NULL DEFAULT 'moderate',
  `fitness_goal` varchar(20) NOT NULL DEFAULT 'maintain',
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password_hash`, `age`, `gender`, `height`, `initial_weight`, `activity_level`, `fitness_goal`, `created_at`) VALUES
(1, 'weikit', 'scrypt:32768:8:1$vpd7WlYlh7QLIpxj$5076ff3a92af08f7ee3d57c6649497e75426a8e5c2d0d83ac2fce939de637d35434e863d2f46c076978212836cc8695ed9e58a1d21891644d8f33e1ad1c91bf8', 22, 'male', 178, 72, 'active', 'maintain', '2026-09-09 13:05:53'),
(2, 'jason', 'scrypt:32768:8:1$aqumcu4yxeDETFVP$e891f062a9c82db97aa99c9632cd5dff9e8921c6454028437e1063e354764f88dc412aa5e52a4496bf9fee8dc10d757db1a6845c39f427eb5add936ba847eb97', 30, 'male', 160, 30, 'sedentary', 'cut', '2026-09-28 12:33:47');

-- --------------------------------------------------------

--
-- Table structure for table `workoutlogs`
--

CREATE TABLE `workoutlogs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `log_date` date NOT NULL,
  `exercise_name` varchar(100) NOT NULL,
  `muscle_group` varchar(20) NOT NULL,
  `sets` int(11) NOT NULL,
  `reps` int(11) NOT NULL,
  `weight_used` float NOT NULL DEFAULT 0
) ;

--
-- Dumping data for table `workoutlogs`
--

INSERT INTO `workoutlogs` (`id`, `user_id`, `log_date`, `exercise_name`, `muscle_group`, `sets`, `reps`, `weight_used`) VALUES
(1, 1, '2026-09-23', '杠铃卧推', '胸部', 4, 15, 50),
(2, 1, '2026-09-23', '杠铃卧推', '胸部', 4, 15, 0),
(3, 1, '2026-09-22', '高位下拉', '背部', 3, 13, 62),
(4, 1, '2026-09-21', '杠铃深蹲', '腿部', 3, 15, 50),
(5, 1, '2026-09-19', '二头弯举', '手臂', 3, 15, 15),
(6, 1, '2026-09-20', '卷腹', '核心', 3, 12, 0),
(7, 1, '2026-09-27', '哑铃飞鸟', '肩部', 3, 15, 10),
(8, 1, '2026-09-27', '二头弯举', '手臂', 10, 15, 9.5),
(9, 1, '2026-09-26', '高位下拉', '背部', 3, 15, 55.5),
(10, 2, '2026-09-27', '上斜卧推', '胸部', 3, 10, 20);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `exercises`
--
ALTER TABLE `exercises`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_exercises_muscle` (`muscle_group`);

--
-- Indexes for table `fooditems`
--
ALTER TABLE `fooditems`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_fooditems_meal` (`meal_type`);

--
-- Indexes for table `healthlogs`
--
ALTER TABLE `healthlogs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_user_date` (`user_id`,`log_date`),
  ADD KEY `idx_healthlogs_user_date` (`user_id`,`log_date`);

--
-- Indexes for table `reporthistory`
--
ALTER TABLE `reporthistory`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_reporthistory_user_date` (`user_id`,`generated_at`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `workoutlogs`
--
ALTER TABLE `workoutlogs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_workoutlogs_user_date` (`user_id`,`log_date`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `exercises`
--
ALTER TABLE `exercises`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `fooditems`
--
ALTER TABLE `fooditems`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `healthlogs`
--
ALTER TABLE `healthlogs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `reporthistory`
--
ALTER TABLE `reporthistory`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `workoutlogs`
--
ALTER TABLE `workoutlogs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `healthlogs`
--
ALTER TABLE `healthlogs`
  ADD CONSTRAINT `fk_healthlogs_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `reporthistory`
--
ALTER TABLE `reporthistory`
  ADD CONSTRAINT `fk_reporthistory_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `workoutlogs`
--
ALTER TABLE `workoutlogs`
  ADD CONSTRAINT `fk_workoutlogs_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
