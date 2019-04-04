# bc-dashboard-indicators
NOTE: These indicators assume you are running OSCAR stable build #849 or something more recent.
The indicators can be loaded individually.  If you want to do that read the documentation in the Documentation folder.  However, it is much easier to setup the dashboard panels and indicators by sourcing the script SQL_Scripts/DoBC_dashboard.sql.  The BC billing indicators can be added by sourcing the script SQL_Scripts/bc_billing_dashboard.sql.  The script SQL_Scripts/config_DoBC_dashboard_permissions.sql can be used to give Oscar users permission to use the dashboard.

When SQL_Scripts/DoBC_dashboard.sql is updated, the DoBC indicator templates at clinics can be updated as follows:

From the folder where you have placed the DoBC_dashboard.sql script on the server
run the mysql command-line in the Oscar database:

<pre>
mysql> delete from dashboard where description='DoBC Panel';
mysql> delete from indicatorTemplate where framework="DoBC CPQI PSP Panel";
mysql> source source DoBC_dashboard.sql
</pre>
