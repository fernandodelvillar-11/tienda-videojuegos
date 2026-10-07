import pymysql
pymysql.install_as_MySQLdb()

# Parche para evitar el error de versión de MariaDB en XAMPP
pymysql.version_info = (10, 11, 0, "final", 0)