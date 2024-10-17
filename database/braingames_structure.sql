--
-- Structure of database creatoion and usage `braingames_db`
--

CREATE DATABASE IF NOT EXISTS `braingames_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `braingames_db`;

--
-- Structure of table `results`
--

CREATE TABLE IF NOT EXISTS `results` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `exercise` VARCHAR(50) NOT NULL,
  `date_hour` DATETIME NOT NULL,
  `duration` TIME NOT NULL,
  `nbtrials` INT(11) NOT NULL,
  `nbok` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
);



--
-- Structure of table `roles`
--

CREATE TABLE IF NOT EXISTS `roles` (
  `id` INT(11) PRIMARY KEY NOT NULL,
  `name` VARCHAR(50) NOT NULL
);



--
-- Structure of table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `pseudo` VARCHAR(50) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `role_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
);
