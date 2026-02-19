# Auto-generated file: error injection for MySQL detection

ERRORS_INJ = {
    "' or 1=1--",
    "')",
    "'",
    '" or "1"="1',
    '"))',
    "' or '1'='1",
    '"--',
    "' union select 1--",
    "' union select null--",
    '`',
    "' order by 1--",
    "' order by 100--",
    "' group by 1--",
    "'--",
    "'))",
    '"',
    '" or 1=1--',
}

SQLITE_ERROR = {
    'errors': ERRORS_INJ,
}
