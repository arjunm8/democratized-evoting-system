CREATE TABLE `document` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int,
  `type` varchar(255) NOT NULL,
  `number` varchar(255) UNIQUE,
  `verified` boolean,
  `created` datetime DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `user` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `phone` varchar(255) UNIQUE,
  `constituency` varchar(255),
  `verified` boolean DEFAULT true,
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
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
  `created` datetime DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `retrospect` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `image_url` varchar(255),
  `ballot_id` int,
  `created` datetime DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `candidate` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255) UNIQUE,
  `image_url` varchar(255),
  `verified` boolean,
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  `constituency_id` int
);

ALTER TABLE `document` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `user` ADD FOREIGN KEY (`constituency_id`) REFERENCES `constituency` (`id`);

ALTER TABLE `ballot` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `ballot` ADD FOREIGN KEY (`candidate_id`) REFERENCES `candidate` (`id`);

ALTER TABLE `retrospect` ADD FOREIGN KEY (`ballot_id`) REFERENCES `ballot` (`id`);

ALTER TABLE `candidate` ADD FOREIGN KEY (`constituency_id`) REFERENCES `constituency` (`id`);
