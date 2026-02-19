# Auto-generated file: error patterns for SQL detection

MYSQL_ERRORS = {
    'check the manual that corresponds to your mysql server version',
    "column count doesn't match value count",
    'duplicate entry',
    'incorrect integer value',
    'mysql server version for the right syntax',
    'mysql_fetch',
    'mysql_num_rows',
    'mysql_query',
    'mysql_result',
    'mysqli_fetch',
    'operand should contain',
    'subquery returns more than 1 row',
    'supplied argument is not a valid mysql',
    'unknown column',
    'warning: mysql',
    'you have an error in your sql syntax',
}

SQLITE_ERRORS = {
    'constraint failed',
    'datatype mismatch',
    'near "',
    'no such column',
    'no such table',
    'order by term out of range',
    'selects to the left and right of union do not have the same number of result columns',
    'sqlite error',
    'sqlite3.databaseerror',
    'sqlite3.integrityerror',
    'sqlite3.operationalerror',
    'syntax error',
    'unrecognized token',
}

ERROR_PATTERNS = {
    'mysql': MYSQL_ERRORS,
    'sqlite': SQLITE_ERRORS,
}
