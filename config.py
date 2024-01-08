MYSQL_CONFIG = {
    'user': 'db_user',
    'password': 'db_passwd',
    'host': 'db_host',
    'database': 'db_name',
}

"""
For the context, the table `sensor_data` has 4 columns:
    * `id`          - PRIMARY KEY, INT, AUTO INCREMENT
    * `temperature` - FLOAT
    * `humidity`    - FLOAT
    * `date`        - DATE.CURRENT_TIMESTAMP()
    * `time`        - TIME.CURRENT_TIMESTAMP()
"""
