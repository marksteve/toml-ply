from datetime import datetime
import ply.lex as lex
import ply.yacc as yacc


tokens = ('KEY',
          'KEYGROUP',
          'EQUALS',
          'BOOLEAN',
          'DATETIME',
          'STRING',
          'INTEGER',
          )
literals = '[,]'


# Lexer

t_ignore = ' \t'
t_KEY = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_EQUALS = r'='

def t_KEYGROUP(t):
    r'\[[a-zA-Z_][a-zA-Z0-9_\.]*\]'
    t.value = t.value[1:-1].split('.')
    return t

def t_BOOLEAN(t):
    r'true|false'
    t.value = t.value == 'true'
    return t

ISO8601_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

def t_DATETIME(t):
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z'
    t.value = datetime.strptime(t.value, ISO8601_FORMAT)
    return t

def t_STRING(t):
    r'"(\\"|[^"])*"'
    t.value = t.value[1:-1].decode('string-escape')
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_comment(t):
    r'\#.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lex.lex()


# Parser

class TOMLParser(object):

    tokens = tokens

    def p_error(self, p):
        pass

    def p_toml(self, p):
        '''toml : assigns'''
        p[0] = self.toml

    def p_assigns(self, p):
        '''assigns : assigns assign
                   | assign'''

    def p_assign(self, p):
        '''assign : KEY EQUALS value
                  | assign KEYGROUP'''
        if isinstance(p[2], list):
            self.keys = p[2]
        else:
            d = self.toml
            if self.keys:
                for k in self.keys:
                    d.setdefault(k, {})
                    d = d[k]
            d[p[1]] = p[3]

    def p_array(self, p):
        '''
        array : '[' array ']'
              | array ',' array
              | array ',' array ','
              | value
              '''
        if len(p) == 2:
            p[0] = p[1]
        elif p[2] == ',':
            # value, value
            if not isinstance(p[1], list) and not isinstance(p[3], list):
                p[0] = [p[1], p[3]]
            # value, array
            elif not isinstance(p[1], list) and isinstance(p[3], list):
                p[0] = [p[1]] + p[3]
            # array, array
            elif isinstance(p[1], list) and isinstance(p[3], list):
                # array, array(array)
                if isinstance(p[3][0], list):
                    p[0] = [p[1]] + p[3]
                else:
                    p[0] = [p[1], p[3]]
        else:
            p[0] = p[2]

    def p_value(self, p):
        '''value : BOOLEAN
                 | DATETIME
                 | STRING
                 | INTEGER
                 | array'''
        p[0] = p[1]

    def __init__(self):
        # FIXME: Turning off write_tables makes this slow
        self.parser = yacc.yacc(module=self, debug=0, write_tables=0)

    def parse(self, s):
        self.toml = dict()
        self.keys = []
        return self.parser.parse(s)


def loads(s):
    return TOMLParser().parse(s)
