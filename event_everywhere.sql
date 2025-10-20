/*
 Navicat Premium Dump SQL

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80041 (8.0.41)
 Source Host           : localhost:3306
 Source Schema         : event_everywhere

 Target Server Type    : MySQL
 Target Server Version : 80041 (8.0.41)
 File Encoding         : 65001

 Date: 04/27/2025 23:30:14
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `event_id` int NULL DEFAULT NULL,
  `user_id` int NULL DEFAULT NULL,
  `content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `event_id`(`event_id` ASC) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for event
-- ----------------------------
DROP TABLE IF EXISTS `event`;
CREATE TABLE `event`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `root_id` int NULL DEFAULT NULL,
  `user_id` int NULL DEFAULT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `category` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `start_at` datetime NULL DEFAULT NULL,
  `end_at` datetime NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `latitude` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `longitude` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `event_ibfk_1`(`root_id` ASC) USING BTREE,
  CONSTRAINT `event_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for like
-- ----------------------------
DROP TABLE IF EXISTS `like`;
CREATE TABLE `like`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `event_id` int NULL DEFAULT NULL,
  `user_id` int NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `event_id`(`event_id` ASC) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `like_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `like_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;

-- password '123456' 

INSERT INTO `user` (`id`, `username`, `password`, `name`, `content`) VALUES (1, 'jiaojh', '$2b$12$SwouOg2Jp51MhITBONdNRuC7A10Hf52qPOy7RgWwaNnpv41r8MiNa', 'James Johnson', 'Enjoys outdoor adventures.');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `content`) VALUES (2, 'sunny_dancer', '$2b$12$SwouOg2Jp51MhITBONdNRuC7A10Hf52qPOy7RgWwaNnpv41r8MiNa', 'Emily Smith', 'Passionate about technology.');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `content`) VALUES (3, 'rocketeer2025', '$2b$12$SwouOg2Jp51MhITBONdNRuC7A10Hf52qPOy7RgWwaNnpv41r8MiNa', 'Michael Williams', 'Loves hiking and photography.');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `content`) VALUES (4, 'lucky_cat', '$2b$12$SwouOg2Jp51MhITBONdNRuC7A10Hf52qPOy7RgWwaNnpv41r8MiNa', 'Sarah Brown', 'Avid reader and coffee enthusiast.');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `content`) VALUES (5, 'blueberrypie', '$2b$12$SwouOg2Jp51MhITBONdNRuC7A10Hf52qPOy7RgWwaNnpv41r8MiNa', 'David Jones', 'Fan of sci-fi movies.');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `content`) VALUES (6, 'the_wanderer', '$2b$12$SwouOg2Jp51MhITBONdNRuC7A10Hf52qPOy7RgWwaNnpv41r8MiNa', 'Linda Garcia', 'Travel blogger and foodie.');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `content`) VALUES (7, 'pixel_master', '$2b$12$SwouOg2Jp51MhITBONdNRuC7A10Hf52qPOy7RgWwaNnpv41r8MiNa', 'Robert Martinez', 'Designs stunning visuals.');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `content`) VALUES (8, 'green_thumb', '$2b$12$SwouOg2Jp51MhITBONdNRuC7A10Hf52qPOy7RgWwaNnpv41r8MiNa', 'Patricia Rodriguez', 'Gardening and DIY lover.');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `content`) VALUES (9, 'storm_chaser', '$2b$12$SwouOg2Jp51MhITBONdNRuC7A10Hf52qPOy7RgWwaNnpv41r8MiNa', 'Christopher Lee', 'Dreams of chasing storms.');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `content`) VALUES (10, 'dream_weaver', '$2b$12$SwouOg2Jp51MhITBONdNRuC7A10Hf52qPOy7RgWwaNnpv41r8MiNa', 'Barbara Walker', 'Writes fantasy novels.');

INSERT INTO `event` (`id`, `root_id`, `user_id`, `title`, `category`, `img`, `content`, `start_at`, `end_at`, `created_at`, `latitude`, `longitude`, `address`) VALUES
(1, 1, 2, 'Central Park Music Festival', 'Outdoor Concert', 'https://picsum.photos/1000', 'Enjoy live music in Central Park.', '2025-05-08 17:00:00', '2025-05-08 21:00:00', '2025-04-29 10:00:00', '40.785091', '-73.968285', 'Central Park, New York, NY 10024'),
(2, 2, 3, 'Times Square Dance Battle', 'Dance Battle', 'https://picsum.photos/1000', 'Show your moves at Times Square!', '2025-05-09 18:00:00', '2025-05-09 21:30:00', '2025-04-29 10:01:00', '40.758896', '-73.985130', 'Times Square, New York, NY 10036'),
(3, 3, 4, 'Union Square Food Festival', 'Food Festival', 'https://picsum.photos/1000', 'Taste foods from around the world.', '2025-05-10 12:00:00', '2025-05-10 18:00:00', '2025-04-29 10:02:00', '40.735863', '-73.991084', 'Union Square, New York, NY 10003'),
(4, 4, 5, '5th Ave Magic Night', 'Magic Show', 'https://picsum.photos/1000', 'Street magic along Fifth Avenue.', '2025-05-11 15:00:00', '2025-05-11 17:30:00', '2025-04-29 10:03:00', '40.774036', '-73.965088', '1000 5th Ave, New York, NY 10028'),
(5, 5, 6, 'SoHo Art Display', 'Art Exhibition', 'https://picsum.photos/1000', 'Contemporary art showcase.', '2025-05-12 11:00:00', '2025-05-12 16:00:00', '2025-04-29 10:04:00', '40.723301', '-74.002988', '99 Prince St, New York, NY 10012'),
(6, 6, 7, 'Bryant Park Movie Night', 'Movie Screening', 'https://picsum.photos/1000', 'Outdoor movie under the stars.', '2025-05-13 19:00:00', '2025-05-13 22:30:00', '2025-04-29 10:05:00', '40.753596', '-73.983232', 'Bryant Park, New York, NY 10018'),
(7, 7, 1, 'Battery Park Carnival', 'Carnival', 'https://picsum.photos/1000', 'Family fun at Battery Park!', '2025-05-14 10:00:00', '2025-05-14 18:00:00', '2025-04-29 10:06:00', '40.703277', '-74.017028', 'Battery Park, New York, NY 10004'),
(8, 8, 9, 'Chelsea Food Truck Rally', 'Food Truck', 'https://picsum.photos/1000', 'Food trucks from all over NYC.', '2025-05-15 12:00:00', '2025-05-15 17:00:00', '2025-04-29 10:07:00', '40.746500', '-74.001374', '75 9th Ave, New York, NY 10011'),
(9, 9, 1, 'Washington Square Parade', 'Parade', 'https://picsum.photos/1000', 'Colorful parade starting at Washington Square.', '2025-05-16 11:00:00', '2025-05-16 14:00:00', '2025-04-29 10:08:00', '40.730823', '-73.997332', 'Washington Square Park, New York, NY 10012'),
(10, 10, 2, 'Broadway Performance Night', 'Performance', 'https://picsum.photos/1000', 'Broadway open-air night.', '2025-05-17 19:00:00', '2025-05-17 22:30:00', '2025-04-29 10:09:00', '40.759011', '-73.984472', '1681 Broadway, New York, NY 10019'),
(11, 11, 3, 'Upper West Side Food Truck Fair', 'Food Truck', 'https://picsum.photos/1000', 'Food truck delights at Upper West Side.', '2025-05-08 12:00:00', '2025-05-08 16:00:00', '2025-04-29 10:10:00', '40.787011', '-73.975368', '200 W 72nd St, New York, NY 10023'),
(12, 12, 4, 'Harlem Street Parade', 'Parade', 'https://picsum.photos/1000', 'Parade celebrating Harlem’s vibrant culture.', '2025-05-09 10:00:00', '2025-05-09 13:00:00', '2025-04-29 10:11:00', '40.811550', '-73.946477', '125th St, New York, NY 10027'),
(13, 13, 5, 'Roosevelt Island Carnival', 'Carnival', 'https://picsum.photos/1000', 'Island carnival fun for all ages.', '2025-05-10 11:00:00', '2025-05-10 17:00:00', '2025-04-29 10:12:00', '40.7622', '-73.9496', '425 Main St, New York, NY 10044'),
(14, 14, 6, 'Lincoln Center Magic Show', 'Magic Show', 'https://picsum.photos/1000', 'Mind-blowing magic at Lincoln Center.', '2025-05-11 14:00:00', '2025-05-11 16:30:00', '2025-04-29 10:13:00', '40.772464', '-73.983489', '10 Lincoln Center Plaza, New York, NY 10023'),
(15, 15, 7, 'East Village Art Walk', 'Art Exhibition', 'https://picsum.photos/1000', 'Street art and gallery showcase.', '2025-05-12 13:00:00', '2025-05-12 18:00:00', '2025-04-29 10:14:00', '40.726477', '-73.981533', '125 E 11th St, New York, NY 10003'),
(16, 16, 8, 'Lower East Side Food Fest', 'Food Festival', 'https://picsum.photos/1000', 'Tasting event across Lower East Side.', '2025-05-13 12:00:00', '2025-05-13 17:00:00', '2025-04-29 10:15:00', '40.717987', '-73.990593', '85 Orchard St, New York, NY 10002'),
(17, 17, 9, 'Chinatown Lantern Parade', 'Parade', 'https://picsum.photos/1000', 'Lantern parade through Chinatown.', '2025-05-14 18:00:00', '2025-05-14 21:00:00', '2025-04-29 10:16:00', '40.715751', '-73.997031', 'Chatham Square, New York, NY 10038'),
(18, 18, 10, 'Hudson Yards Music Night', 'Outdoor Concert', 'https://picsum.photos/1000', 'Live outdoor concert at Hudson Yards.', '2025-05-15 19:00:00', '2025-05-15 23:00:00', '2025-04-29 10:17:00', '40.754205', '-74.002188', '20 Hudson Yards, New York, NY 10001'),
(19, 19, 2, 'Battery Park Movie Screening', 'Movie Screening', 'https://picsum.photos/1000', 'Enjoy an open-air movie night.', '2025-05-16 20:00:00', '2025-05-16 23:00:00', '2025-04-29 10:18:00', '40.703277', '-74.017028', 'Battery Park, New York, NY 10004'),
(20, 20, 3, 'Meatpacking District Food Rally', 'Food Truck', 'https://picsum.photos/1000', 'Food trucks in the Meatpacking District.', '2025-05-17 12:00:00', '2025-05-17 16:00:00', '2025-04-29 10:19:00', '40.740083', '-74.007523', '837 Washington St, New York, NY 10014'),

(21, 21, 4, 'Columbus Circle Parade', 'Parade', 'https://picsum.photos/1000', 'A colorful celebration at Columbus Circle.', '2025-05-08 14:00:00', '2025-05-08 17:00:00', '2025-04-29 10:20:00', '40.768044', '-73.981893', 'Columbus Circle, New York, NY 10019'),
(22, 22, 5, 'Hell\'s Kitchen Carnival', 'Carnival', 'https://picsum.photos/1000', 'Games, food, and rides at the carnival.', '2025-05-09 10:00:00', '2025-05-09 18:00:00', '2025-04-29 10:21:00', '40.763795', '-73.991043', '9th Ave, New York, NY 10019'),
(23, 23, 6, 'Midtown Magic Show', 'Magic Show', 'https://picsum.photos/1000', 'Unbelievable tricks and illusions.', '2025-05-10 16:00:00', '2025-05-10 19:00:00', '2025-04-29 10:22:00', '40.754932', '-73.984016', '450 W 33rd St, New York, NY 10001'),
(24, 24, 7, 'Financial District Art Exhibit', 'Art Exhibition', 'https://picsum.photos/1000', 'Street art meets skyscrapers.', '2025-05-11 11:00:00', '2025-05-11 17:00:00', '2025-04-29 10:23:00', '40.707491', '-74.011276', '140 Broadway, New York, NY 10005'),
(25, 25, 8, 'Little Italy Food Fest', 'Food Festival', 'https://picsum.photos/1000', 'Celebrate Italian cuisine.', '2025-05-12 13:00:00', '2025-05-12 18:00:00', '2025-04-29 10:24:00', '40.719141', '-73.997327', 'Mulberry St, New York, NY 10013'),
(26, 26, 9, 'Gramercy Outdoor Concert', 'Outdoor Concert', 'https://picsum.photos/1000', 'Enjoy music at Gramercy Park.', '2025-05-13 18:00:00', '2025-05-13 21:00:00', '2025-04-29 10:25:00', '40.7376', '-73.9846', '2 Lexington Ave, New York, NY 10010'),
(27, 27, 10, 'Stuyvesant Town Movie Screening', 'Movie Screening', 'https://picsum.photos/1000', 'Outdoor movie fun for families.', '2025-05-14 19:30:00', '2025-05-14 22:00:00', '2025-04-29 10:26:00', '40.7312', '-73.9787', '14th St & 1st Ave, New York, NY 10009'),
(28, 28, 2, 'Madison Square Park Food Trucks', 'Food Truck', 'https://picsum.photos/1000', 'Gourmet food trucks in the park.', '2025-05-15 11:30:00', '2025-05-15 16:00:00', '2025-04-29 10:27:00', '40.7425', '-73.9880', '11 Madison Ave, New York, NY 10010'),
(29, 29, 3, 'Garment District Parade', 'Parade', 'https://picsum.photos/1000', 'Fashion-themed street parade.', '2025-05-16 13:00:00', '2025-05-16 16:30:00', '2025-04-29 10:28:00', '40.7527', '-73.9917', 'Fashion Ave, New York, NY 10018'),
(30, 30, 4, 'Yorkville Street Festival', 'Carnival', 'https://picsum.photos/1000', 'Carnival with local vendors and games.', '2025-05-17 12:00:00', '2025-05-17 17:00:00', '2025-04-29 10:29:00', '40.7750', '-73.9500', '86th St, New York, NY 10028');



INSERT INTO `comment` (`id`, `event_id`, `user_id`, `content`, `created_at`) VALUES
(1, 1, 3, 'Looking forward to this event!', '2025-04-05 14:30:00'),
(2, 2, 6, 'This sounds amazing!', '2025-04-06 09:20:00'),
(3, 3, 5, 'Can’t wait!', '2025-04-08 11:45:00'),
(4, 4, 2, 'Registered already!', '2025-04-09 10:00:00'),
(5, 5, 8, 'Will there be parking available?', '2025-04-10 16:20:00'),
(6, 6, 1, 'My kids would love this.', '2025-04-12 13:15:00'),
(7, 7, 9, 'Hope to find investors!', '2025-04-13 15:50:00'),
(8, 8, 10, 'Very excited about this!', '2025-04-14 08:30:00'),
(9, 9, 4, 'Perfect event for weekend.', '2025-04-16 17:10:00'),
(10, 10, 7, 'Can beginners join too?', '2025-04-17 12:05:00'),
(11, 1, 3, 'Looking forward to this event!', '2025-04-05 14:30:00'),
(12, 2, 6, 'This sounds amazing!', '2025-04-06 09:20:00'),
(13, 3, 5, 'Can’t wait!', '2025-04-08 11:45:00'),
(14, 4, 2, 'Registered already!', '2025-04-09 10:00:00'),
(15, 5, 8, 'Will there be parking available?', '2025-04-10 16:20:00'),
(16, 6, 1, 'My kids would love this.', '2025-04-12 13:15:00'),
(17, 7, 9, 'Hope to find investors!', '2025-04-13 15:50:00'),
(18, 8, 10, 'Very excited about this!', '2025-04-14 08:30:00'),
(19, 9, 4, 'Perfect event for weekend.', '2025-04-16 17:10:00'),
(20, 10, 7, 'Can beginners join too?', '2025-04-17 12:05:00');


INSERT INTO `like` (`id`, `event_id`, `user_id`, `created_at`) VALUES
(1, 1, 4, '2025-04-03 16:45:00'),
(2, 2, 7, '2025-04-04 12:10:00'),
(3, 3, 2, '2025-04-05 09:00:00'),
(4, 4, 5, '2025-04-06 18:20:00'),
(5, 5, 1, '2025-04-07 14:30:00'),
(6, 6, 6, '2025-04-08 10:40:00'),
(7, 7, 8, '2025-04-09 11:50:00'),
(8, 8, 9, '2025-04-10 17:30:00'),
(9, 9, 3, '2025-04-11 16:00:00'),
(10, 10, 10, '2025-04-12 13:15:00'),
(11, 1, 4, '2025-04-03 16:45:00'),
(12, 2, 7, '2025-04-04 12:10:00'),
(13, 3, 2, '2025-04-05 09:00:00'),
(14, 4, 5, '2025-04-06 18:20:00'),
(15, 5, 1, '2025-04-07 14:30:00'),
(16, 6, 6, '2025-04-08 10:40:00'),
(17, 7, 8, '2025-04-09 11:50:00'),
(18, 8, 9, '2025-04-10 17:30:00'),
(19, 9, 3, '2025-04-11 16:00:00'),
(20, 10, 10, '2025-04-12 13:15:00');

