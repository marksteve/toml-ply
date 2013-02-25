import ply.lex as lex
import ply.yacc as yacc


tokens = ('KEY',
          'KEYGROUP',
          'EQUALS',
          'INTEGER',
          )


# Lexer

t_ignore = ' \t'
t_KEY = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_EQUALS = r'='

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_KEYGROUP(t):
    r'\[[a-zA-Z_][a-zA-Z0-9_\.]*\]'
    t.value = t.value[1:-1].split('.')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lex.lex()


# Parser

toml = dict()
keys = []

def p_toml(p):
    '''toml : assigns'''
    p[0] = toml

def p_assigns(p):
    '''assigns : assigns assign
               | assign'''

def p_assign(p):
    '''assign : KEY EQUALS value
              | assign KEYGROUP'''
    if isinstance(p[2], list):
        global keys
        keys = p[2]
    else:
        d = toml
        if keys:
            for k in keys:
                d.setdefault(k, {})
                d = d[k]
        d[p[1]] = p[3]

def p_value(p):
    '''value : INTEGER'''
    p[0] = p[1]

parser = yacc.yacc()


def loads(s):
    return parser.parse(s)
