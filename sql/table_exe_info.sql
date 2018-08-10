/*
Navicat MySQL Data Transfer

Source Server         : etlmetadata
Source Server Version : 50717
Source Host           : 192.168.0.58:3306
Source Database       : etlmetadata

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2018-07-27 14:14:40
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for table_exe_info
-- ----------------------------
DROP TABLE IF EXISTS `table_exe_info`;
CREATE TABLE `table_exe_info` (
  `id` bigint(10) NOT NULL AUTO_INCREMENT,
  `sourceTableName` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `targetTableName` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sourceDBName` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `targetDBName` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type` int(2) DEFAULT '0' COMMENT '1创建表，2全表导入数据，3导入数据到临时表，4合并临时表以及全表',
  `batchNum` bigint(10) DEFAULT '0' COMMENT '第N次批次序号，启动一次命令一个批号',
  `status` int(2) DEFAULT '0' COMMENT '0还没有开始启动执行，1执行中，2执行成功，3执行失败',
  `gmt_create` datetime DEFAULT CURRENT_TIMESTAMP,
  `gmt_modify` datetime DEFAULT CURRENT_TIMESTAMP,
  `startTime` datetime DEFAULT NULL COMMENT '命令启动时间',
  `endTime` datetime DEFAULT NULL COMMENT '命令时间束',
  `useTime` bigint(20) DEFAULT NULL COMMENT 'int((endTime.microsecond-startTime.microsecond)/1000)',
  `cmd` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `stn_idx` (`sourceTableName`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8259 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of table_exe_info
-- ----------------------------
