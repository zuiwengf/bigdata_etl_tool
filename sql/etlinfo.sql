/*
Navicat MySQL Data Transfer

Source Server         : etlinfo
Source Server Version : 50717
Source Host           : 192.168.0.2:3306
Source Database       : etlinfo

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2018-07-27 16:09:33
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
INSERT INTO `app_config` VALUES ('1', 'd:/mytest', '/xxxx/xxxx', 'hdfs://192.168.0.2:8020', 'dev', '2018-07-19 15:49:32', '2018-07-19 15:49:36');
INSERT INTO `app_config` VALUES ('2', '/tmp/OdsSqoopTool', '/xxxx/xxxx', 'hdfs://192.168.0.2:8020', 'test', '2018-07-20 12:21:59', '2018-07-20 12:22:01');
INSERT INTO `app_config` VALUES ('3', '/data/etlmetadata/logs', '/data/etlmetadata/logs', 'hdfs://192.168.0.2:8020', 'production', '2018-07-20 12:22:04', '2018-07-20 12:22:06');

-- ----------------------------
-- Table structure for etl_db
-- ----------------------------
DROP TABLE IF EXISTS `etl_db`;
CREATE TABLE `etl_db` (
  `id` int(5) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `dbName` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '数据库名称',
  `dbHost` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '数据库ip',
  `dbPort` int(6) DEFAULT '3306' COMMENT '数据库端口',
  `userName` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '数据库连接用户名',
  `password` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户密码',
  `gmt_modify` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
  `gmt_create` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `enable` smallint(1) DEFAULT '1' COMMENT '是否启用',
  `torder` int(6) DEFAULT '100' COMMENT '扫描的顺序',
  PRIMARY KEY (`id`),
  UNIQUE KEY `dbName_idx` (`dbName`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='creator:zuiweng.df';

-- ----------------------------
-- Records of etl_db
-- ----------------------------
INSERT INTO `etl_db` VALUES ('2', 'tb1', '192.168.0.2', '3306', 'user1', 'user1@2018', '2018-07-19 15:51:53', '2018-07-19 15:51:53', '1', '100');
INSERT INTO `etl_db` VALUES ('3', 'tb2', '192.168.0.2', '3306', 'user1', 'user1@2018', '2018-07-19 15:52:28', '2018-07-19 15:52:28', '1', '100');
INSERT INTO `etl_db` VALUES ('4', 'tb3', '192.168.0.2', '3306', 'user1', 'user1@2018', '2018-07-19 15:53:32', '2018-07-19 15:53:32', '1', '100');
INSERT INTO `etl_db` VALUES ('5', 'tb4', '192.168.0.58', '3306', 'user1', 'user1@2018', '2018-07-19 15:54:00', '2018-07-19 15:54:00', '1', '100');

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
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='creator:zuiweng.df';

-- ----------------------------
-- Records of etl_table_template
-- ----------------------------
INSERT INTO `etl_table_template` VALUES ('1', 'table1', '2', null, 'id', '0', null, 'gmt_modify', '1', '1', '1', '1', '4', '100000', '1', '2018-07-19 15:54:55', '2018-07-19 15:54:55');
INSERT INTO `etl_table_template` VALUES ('8', 'table2', '3', '_00', 'id', '1', 'id', 'gmt_modify', '1', '1', '1', '1', '4', '50', '1', '2018-07-19 15:59:57', '2018-07-19 15:59:57');
INSERT INTO `etl_table_template` VALUES ('9', 'table3', '3', '_00', 'id', '1', 'id', 'gmt_modify', '1', '1', '1', '1', '4', '100', '1', '2018-07-19 16:00:21', '2018-07-19 16:00:21');
INSERT INTO `etl_table_template` VALUES ('10', 'table4', '4', null, 'id', '0', null, 'gmt_modify', '1', '1', '1', '1', '4', '10', '1', '2018-07-19 16:01:28', '2018-07-19 16:01:28');
INSERT INTO `etl_table_template` VALUES ('11', 'table5', '4', null, 'id', '0', null, 'gmt_modify', '1', '1', '1', '1', '4', '100', '1', '2018-07-19 16:01:49', '2018-07-19 16:01:49');
INSERT INTO `etl_table_template` VALUES ('12', 'table6', '5', '_00', 'id', '1', 'id', 'gmt_modify', '1', '1', '1', '1', '4', '100', '1', '2018-07-19 16:02:19', '2018-07-19 16:02:19');
INSERT INTO `etl_table_template` VALUES ('13', 'table7', '5', '_00', 'id', '1', 'id', 'gmt_modify', '1', '1', '1', '1', '4', '100', '1', '2018-07-19 16:02:40', '2018-07-19 16:02:40');

-- Table structure for exe_batch_info
-- ----------------------------
DROP TABLE IF EXISTS `exe_batch_info`;
CREATE TABLE `exe_batch_info` (
  `batchNum` bigint(10) NOT NULL AUTO_INCREMENT,
  `gmt_create` datetime DEFAULT CURRENT_TIMESTAMP,
  `gmt_modify` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`batchNum`)
) ENGINE=InnoDB AUTO_INCREMENT=152 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='creator:zuiweng.df';

-- ----------------------------
-- Records of exe_batch_info
-- ----------------------------
INSERT INTO `exe_batch_info` VALUES ('149', '2018-07-27 14:20:14', '2018-07-27 14:20:14');
INSERT INTO `exe_batch_info` VALUES ('150', '2018-07-27 14:50:30', '2018-07-27 14:50:30');
INSERT INTO `exe_batch_info` VALUES ('151', '2018-07-27 15:32:29', '2018-07-27 15:32:29');

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
) ENGINE=InnoDB AUTO_INCREMENT=8694 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of table_exe_info
-- ----------------------------
INSERT INTO `table_exe_info` VALUES ('8259', 'table1', 't_phoneuser', 'tb1', 'ods_tb1', '0', '149', '0', '2018-07-27 14:30:23', '2018-07-27 14:30:23', '2018-07-27 14:30:13', '2018-07-27 14:30:23', '9', ' hive -e  \" create EXTERNAL table  IF NOT EXISTS  ods_tb1.t_phoneuser (  id   int  ,  loginId   string  ,  loginType   string  ,  pwd   string  ,  img   string  ,  nickName   string  ,  deviceId   string  ,  phoneType   string  ,  phoneSystem   string  ,  phoneNumber   string  ,  updateTime   timestamp  ,  addTime   timestamp  ,  channels   string  ,  channelType   int  ,  verison   string  ,  telType   int  ,  idfa   string  ,  build   string  ,  quartzStatus   int  ,  state   int  ,  isNew   int  ,  appState   int  ,  city   string  ,  cid   int  ,  lables   string  ,  labels   string  ,  phone   string  ) ROW FORMAT DELIMITED FIELDS TERMINATED BY \'\\t\'  STORED AS TEXTFILE \"   ');
INSERT INTO `table_exe_info` VALUES ('8260', 'table2', 't_phoneuser', 'tb1', 'ods_tb1', '0', '149', '0', '2018-07-27 14:30:34', '2018-07-27 14:30:34', '2018-07-27 14:30:24', '2018-07-27 14:30:35', '10', ' hive -e  \" create EXTERNAL table  IF NOT EXISTS  ods_tb1.t_phoneuser_daily_incr (  id   int  ,  loginId   string  ,  loginType   string  ,  pwd   string  ,  img   string  ,  nickName   string  ,  deviceId   string  ,  phoneType   string  ,  phoneSystem   string  ,  phoneNumber   string  ,  updateTime   timestamp  ,  addTime   timestamp  ,  channels   string  ,  channelType   int  ,  verison   string  ,  telType   int  ,  idfa   string  ,  build   string  ,  quartzStatus   int  ,  state   int  ,  isNew   int  ,  appState   int  ,  city   string  ,  cid   int  ,  lables   string  ,  labels   string  ,  phone   string  ) ROW FORMAT DELIMITED FIELDS TERMINATED BY \'\\t\'  STORED AS TEXTFILE \"   ');
I