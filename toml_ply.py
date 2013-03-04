from datetime import datetime
import ply.lex as lex
import ply.yacc as yacc


tokens = ('KEY',
          'KEYGROUP',
          'EQUALS',
          'BOOLEAN',
          'DATETIME',
          'STRING',
          'FLOAT',
          'INTEGER',
          )
literals = '[,]'


# Lexer

t_ignore = ' \t'

def t_comment(t):
    r'\#.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    raise SyntaxError(repr(t))

t_EQUALS = r'='

def t_BOOLEAN(t):
    r'true|false'
    t.value = t.value == 'true'
    return t

def t_KEY(t):
    r'[a-zA-Z_][a-zA-Z0-9_#\?]*'
    return t

def t_KEYGROUP(t):
    r'\[([a-zA-Z_][a-zA-Z0-9_#\?]*\.?)+\]'
    t.value = tuple(t.value[1:-1].split('.'))
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

def t_FLOAT(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

lex.lex()


# Parser

class TOMLParser(object):

    tokens = tokens

    def p_error(self, p):
        raise SyntaxError(repr(p))

    def p_start(self, p):
        '''start : assigns'''
        p[0] = self.mapping

    def p_assigns(self, p):
        '''assigns : assigns assign
                   | assign'''

    def __check_keygroup(self, keygroup):
        if keygroup in self.keygroups:
            return False
        else:
            return True

    def p_assign(self, p):
        '''assign : KEY EQUALS value
                  | assign KEYGROUP
                  | KEYGROUP'''
        if isinstance(p[1], tuple):
            if not self.__check_keygroup(p[1]):
                raise SyntaxError
            self.keygroups.add(p[1])
            self.keygroup = p[1]
        elif isinstance(p[2], tuple):
            if not self.__check_keygroup(p[2]):
                raise SyntaxError
            self.keygroups.add(p[2])
            self.keygroup = p[2]
        else:
            d = self.mapping
            if self.keygroup:
                for k in self.keygroup:
                    d.setdefault(k, {})
                    d = d[k]
            if p[1] in d:
                raise SyntaxError
            d[p[1]] = p[3]

    def p_array(self, p):
        '''array : '[' seq ']'
                 '''
        p[0] = p[2]

    def p_seq(self, p):
        '''seq : value ',' seq
               | value ','
               | value
               |'''
        if len(p) < 4:
            if len(p) == 1:
                p[0] = []
            else:
                p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_value(self, p):
        '''value : array
                 | BOOLEAN
                 | DATETIME
                 | STRING
                 | FLOAT
                 | INTEGER'''
        p[0] = p[1]

    def __init__(self):
        # FIXME: Turning off write_tables makes this slow
        self.parser = yacc.yacc(module=self, debug=0, write_tables=0)

    def parse(self, s):
        # Reset mapping andkeygroup 
        self.mapping= dict()
        self.keygroup = tuple()
        self.keygroups = set()
        return self.parser.parse(s)


def loads(s):
    return TOMLParser().parse(s)
