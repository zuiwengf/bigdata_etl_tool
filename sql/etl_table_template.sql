/*
Navicat MySQL Data Transfer

Source Server         : etlmetadata
Source Server Version : 50717
Source Host           : 192.168.0.58:3306
Source Database       : etlmetadata

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2018-08-06 17:31:47
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for etl_table_template
-- ----------------------------
DROP TABLE IF EXISTS `etl_table_template`;
CREATE TABLE `etl_table_template` (
  `id` bigint(10) NOT NULL AUTO_INCREMENT,
  `tableName` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '原始表名',
  `dbId` int(6) DEFAULT '0' COMMENT '表所在的数据库id对应etl_db的id',
  `tableSubName` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '分表的后缀字符：_1,_00, _001',
  `pkeyName` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '表对应的主键',
  `isMutTable` smallint(1) DEFAULT '0' COMMENT '是否为多个分表，如xxxx_01,xxxx_02等',
  `mergeCol` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'hive中分桶的列明',
  `incrementCol` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '增量etl时候的使用哪个列来做为数据时修改增加的',
  `incrementType` int(2) DEFAULT '1' COMMENT '增量列的类型： 1是时间类型， 2是Id自动增加的int',
  `createTable` smallint(1) DEFAULT '0' COMMENT '是否需要创建hive表',
  `etlAllData` smallint(2) DEFAULT '0' COMMENT '是全量导入数据，1全量， 0不进行增量',
  `etlIncreamData` smallint(2) DEFAULT '1' COMMENT '是否进进行行增量增加数据，如果1则进行增量导入，0则不进行导入',
  `mapperCount` int(3) DEFAULT '4' COMMENT 'mr时候mapper个数',
  `torder` int(6) DEFAULT '100' COMMENT 'etl顺序',
  `enable` smallint(1) DEFAULT '1' COMMENT '是否启用该表',
  `gmt_modify` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
  `gmt_create` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tableName_idx` (`tableName`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='creator:zuiweng.df';

-- ----------------------------
-- Records of etl_table_template
-- ----------------------------
INSERT INTO `etl_table_template` VALUES ('1', 't_phoneuser', '2', 'XXXXX', 'id', '0', null, 'updateTime', '1', '1', '1', '0', '4', '1000', '1', '2018-07-19 15:54:55', '2018-07-19 15:54:55');
INSERT INTO `etl_table_template` VALUES ('7', 'csl_data_basic', '3', '_00', 'id', '1', 'id', 'gmt_modify', '1', '1', '1', '0', '4', '1000', '1', '2018-07-19 15:59:21', '2018-07-19 15:59:21');
