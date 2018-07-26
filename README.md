# bigdata_etl_tool
从大量的不同的数据库不同表中，抽取数据到ods层。让你从大量配置askaba或oozie中解放出来，只需要简单配置下数据库。
etlmetadata.sql是数据库etl元数据信息


startEtl.sh启动


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



DROP TABLE IF EXISTS `etl_table_template`;
CREATE TABLE `etl_table_template` (
  `id` bigint(10) NOT NULL AUTO_INCREMENT,
  `tableName` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '原始表名',
  `dbId` int(6) DEFAULT '0' COMMENT '表所在的数据库id对应etl_db的id',
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
