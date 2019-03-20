/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE IF NOT EXISTS `dashboard` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `creator` varchar(11) DEFAULT NULL,
  `edited` datetime DEFAULT NULL,
  `active` bit(1) DEFAULT NULL,
  `locked` bit(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
/*!40101 SET character_set_client = @saved_cs_client */;
SET @oscardoc_provider_no='999998';
INSERT INTO `dashboard` (`name`, `description`, `creator`, `edited`, `active`, `locked`) VALUES ('Panel Mgmt 1 - Active Pts, Assigned Provider, Pt Contact Info, Polypharm, Advance Care Planning, Frailty','DoBC Panel',@oscardoc_provider_no,NOW(),'','\0');
SET @dashboardId1 = LAST_INSERT_ID();
INSERT INTO `dashboard` (`name`, `description`, `creator`, `edited`, `active`, `locked`) VALUES ('Panel Mgmt 2 - BP, CHF, DM, COPD, CKD, Ischemic Heart dz, Liver dz, Cerebrovasc dz','DoBC Panel',@oscardoc_provider_no,NOW(),'','\0');
SET @dashboardId2 = LAST_INSERT_ID();
INSERT INTO `dashboard` (`name`, `description`, `creator`, `edited`, `active`, `locked`) VALUES ('Panel Mgmt 3 - OA, Chronic Pain, Anxiety, Depression, Drug and Alcohol Dependence, Dementia','DoBC Panel',@oscardoc_provider_no,NOW(),'','\0');
SET @dashboardId3 = LAST_INSERT_ID();
INSERT INTO `dashboard` (`name`, `description`, `creator`, `edited`, `active`, `locked`) VALUES ('Panel Mgmt Reports -Pop Histogram, Aggregate Spreadsheets for Pt Contact and Primary Provider','DoBC Panel',@oscardoc_provider_no,NOW(),'','\0');
SET @dashboardId4 = LAST_INSERT_ID();
INSERT INTO `dashboard` (`name`, `description`, `creator`, `edited`, `active`, `locked`) VALUES ('Panel Tools','DoBC Panel',@oscardoc_provider_no,NOW(),'','\0');
SET @dashboardId5 = LAST_INSERT_ID();
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE IF NOT EXISTS `indicatorTemplate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dashboardId` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `subCategory` varchar(255) DEFAULT NULL,
  `framework` varchar(255) DEFAULT NULL,
  `frameworkVersion` date DEFAULT NULL,
  `definition` tinytext,
  `notes` tinytext,
  `template` mediumtext,
  `active` bit(1) DEFAULT NULL,
  `locked` bit(1) DEFAULT NULL,
  `shared` tinyint(1) DEFAULT NULL,
  `metricSetName` varchar(255) DEFAULT NULL,
  `metricLabel` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `indicatorTemplate`
--
-- WHERE:  dashboardId!=(select id from dashboard where name='BC Billing – CDMs, 14066, 14076,14078')

LOCK TABLES `indicatorTemplate` WRITE;
{indicator_insert_statements}
UNLOCK TABLES;
