CREATE TABLE `user_savings` (
  `user_id` varchar(50) NOT NULL,
  `account_id` varchar(50) NOT NULL,
  `record_date` datetime(6) NOT NULL,
  `savings_delta` float NOT NULL,
  PRIMARY KEY (`user_id`, `account_id`, `record_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;