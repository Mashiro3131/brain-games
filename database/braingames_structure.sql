--
-- Structure of database creatoion and usage `braingames_db`
--

CREATE DATABASE IF NOT EXISTS `braingames_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `braingames_db`;



--
-- Structure of table `results`
--

CREATE TABLE `results` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `exercise` varchar(50) NOT NULL,
  `date_hour` datetime NOT NULL,
  `duration` time NOT NULL,
  `nbtrials` int(11) NOT NULL,
  `nbok` int(11) NOT NULL
);



--
-- Structure of table `roles`
--

CREATE TABLE `roles` (
  `id` int(11) PRIMARY KEY NOT NULL,
  `name` varchar(50) NOT NULL
);



--
-- Structure of table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `pseudo` varchar(50) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role_id` int(11) NOT NULL
);



--
-- Structure of constraints
--

ALTER TABLE `results` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `users` ADD FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);
