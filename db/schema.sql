CREATE TABLE `document` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int,
  `kind` varchar(255) NOT NULL,
  `number` varchar(255) UNIQUE,
  `image_url` varchar(255),
  `created` datetime DEFAULT (current_timestamp)
);

CREATE TABLE `user` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `phone` varchar(255) UNIQUE,
  `created` datetime DEFAULT (current_timestamp),
  `constituency_id` int
);

CREATE TABLE `constituency` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255) NOT NULL
);

CREATE TABLE `ballot` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int,
  `candidate_id` int,
  `image_url` varchar(255),
  `created` datetime DEFAULT (current_timestamp),
  `transaction_id` varchar(255)
);

CREATE TABLE `candidate` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255) UNIQUE,
  `image_url` varchar(255),
  `created` datetime DEFAULT (current_timestamp),
  `constituency_id` int
);

ALTER TABLE `document` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `user` ADD FOREIGN KEY (`constituency_id`) REFERENCES `constituency` (`id`);

ALTER TABLE `ballot` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `ballot` ADD FOREIGN KEY (`candidate_id`) REFERENCES `candidate` (`id`);

ALTER TABLE `candidate` ADD FOREIGN KEY (`constituency_id`) REFERENCES `constituency` (`id`);

ALTER TABLE `user` ADD FOREIGN KEY (`phone`) REFERENCES `user` (`id`);
