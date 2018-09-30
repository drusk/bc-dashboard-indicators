-- give admin and doctor roles access to dashboard
insert into `secObjPrivilege` values('admin', '_dashboardManager', 'x', 0, '999998') ON DUPLICATE KEY UPDATE objectName='_dashboardManager' ;
insert into `secObjPrivilege` values('admin', '_dashboardDisplay', 'x', 0, '999998') ON DUPLICATE KEY UPDATE objectName='_dashboardDisplay' ;
insert into `secObjPrivilege` values('admin', '_dashboardDrilldown', 'x', 0, '999998') ON DUPLICATE KEY UPDATE objectName='_dashboardDrilldown' ;
insert into `secObjPrivilege` values('doctor', '_dashboardManager', 'r', 0, '999998') ON DUPLICATE KEY UPDATE objectName='_dashboardManager' ;
insert into `secObjPrivilege` values('doctor', '_dashboardDisplay', 'x', 0, '999998') ON DUPLICATE KEY UPDATE objectName='_dashboardDisplay' ;
insert into `secObjPrivilege` values('doctor', '_dashboardDrilldown', 'x', 0, '999998') ON DUPLICATE KEY UPDATE objectName='_dashboardDrilldown' ;
-- setup some dashboards
INSERT INTO `dashboard` (name, description, creator, edited, active, locked) VALUES ('DoBC CPQI PSP Panel 1','','999998',NOW(),'','\0');
INSERT INTO `dashboard` (name, description, creator, edited, active, locked) VALUES ('DoBC CPQI PSP Panel 2','','999998',NOW(),'','\0');
INSERT INTO `dashboard` (name, description, creator, edited, active, locked) VALUES ('DoBC CPQI PSP Panel 3','','999998',NOW(),'','\0');
INSERT INTO `dashboard` (name, description, creator, edited, active, locked) VALUES ('PSP Reports','','999998',NOW(),'','\0');
