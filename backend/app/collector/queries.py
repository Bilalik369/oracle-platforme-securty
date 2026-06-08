"""Requêtes SQL Oracle (vues dynamiques V$/DBA_*)."""

SESSIONS = """
SELECT COUNT(*),
       SUM(CASE WHEN status='ACTIVE' THEN 1 ELSE 0 END),
       SUM(CASE WHEN blocking_session IS NOT NULL THEN 1 ELSE 0 END)
FROM v$session WHERE type='USER'
"""

CPU = ("SELECT value FROM v$sysmetric "
       "WHERE metric_name='Host CPU Utilization (%)' AND group_id=2")

TPS = ("SELECT value FROM v$sysmetric "
       "WHERE metric_name='User Transaction Per Sec' AND group_id=2")

LOCKS = "SELECT COUNT(*) FROM v$lock WHERE block=1"

TABLESPACES = """
SELECT df.tablespace_name, ROUND(df.mb,2),
       ROUND(df.mb-NVL(fs.mb,0),2),
       ROUND((df.mb-NVL(fs.mb,0))/df.mb*100,2)
FROM (SELECT tablespace_name, SUM(bytes)/1048576 mb FROM dba_data_files
        GROUP BY tablespace_name) df
LEFT JOIN (SELECT tablespace_name, SUM(bytes)/1048576 mb FROM dba_free_space
        GROUP BY tablespace_name) fs ON df.tablespace_name=fs.tablespace_name
ORDER BY 4 DESC
"""

PING = "SELECT 1 FROM dual"
