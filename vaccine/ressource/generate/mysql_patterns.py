# Auto-generated file: error injection for MySQL detection

ERRORS_INJ = {
    "'--",
    '"',
    "' or '1'='1",
    '`',
    '" or "1"="1',
    "'#",
    '")',
    '"#',
    "'",
    '" or 1=1--',
    "' or 1=1--",
    "')",
    "'))",
    "' group by 1--",
    '"--',
    "' order by 100--",
    "' order by 1--",
}

MYSQL_ERROR = {
    'errors': ERRORS_INJ,
}
