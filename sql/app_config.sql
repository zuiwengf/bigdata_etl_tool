/*
Navicat MySQL Data Transfer

Source Server         : etlmetadata
Source Server Version : 50717
Source Host           : 192.168.0.58:3306
Source Database       : etlmetadata

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2018-07-30 16:43:59
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for app_config
-- ----------------------------
DROP TABLE IF EXISTS `app_config`;
CREATE TABLE `app_config` (
  `id` bigint(10) NOT NULL AUTO_INCREMENT,
  `etlLogPath` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'etl日志写入的目录',
  `newDataTempDir` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'etl导入hdfs临时目录',
  `namenodeUrl` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'hadoop namenode hdfs url',
  `envName` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'dev,test,production',
  `gmt_modify` datetime DEFAULT NULL,
  `gmt_create` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `envName_idx` (`envName`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='creator:zuiweng.df';

-- ----------------------------
-- Records of app_config
-- ----------------------------
INSERT INTO `app_config` VALUES ('1', 'd:/mytest', '/xxxx/xxxx', 'hdfs://dev-4:8020', 'dev', '2018-07-19 15:49:32', '2018-07-19 15:49:36');
INSERT INTO `app_config` VALUES ('2', '/tmp/OdsSqoopTool', '/xxxx/xxxx', 'hdfs://test:8020', 'test', '2018-07-20 12:21:59', '2018-07-20 12:22:01');
INSERT INTO `app_config` VALUES ('3', '/data/etlmetadata/logs', '/data/etlmetadata/logs', 'hdfs://production-namenode02:8020', 'production', '2018-07-20 12:22:04', '2018-07-20 12:22:06');
