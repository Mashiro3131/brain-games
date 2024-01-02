--
-- Data of table `results`
--

INSERT INTO `results` (`id`, `user_id`, `exercise`, `date_hour`, `duration`, `nbtrials`, `nbok`) VALUES
(1, 1, 'GEO01', '2023-12-04 00:00:00', '00:02:00', 2, 1),
(3, 1, 'INFO05', '2023-12-04 00:00:00', '00:02:00', 2, 1),
(4, 1, 'GEO01', '2023-12-04 00:00:00', '00:02:00', 2, 1),
(5, 1, 'GEO01', '2023-12-04 00:00:00', '00:02:00', 3, 1),
(6, 2, 'GEO01', '2023-12-16 17:45:42', '00:00:02', 2, 0);



--
-- Data of table `roles`
--

INSERT INTO `roles` (`id`, `name`) VALUES
(1, 'student'),
(2, 'teacher'),
(3, 'guest'),
(4, 'administrator');



--
-- Data of table `users`
--

INSERT INTO `users` (`id`, `pseudo`, `password`, `role_id`) VALUES
(1, 'Nico', '1234', 1),
(2, 'Anthony', NULL, 1),
(3, 'Mengisen', NULL, 1);