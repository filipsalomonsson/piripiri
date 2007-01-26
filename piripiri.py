#!/usr/bin/env python
"""Python source code pretty-printer."""

import sys
import tokenize
from token import tok_name
import keyword

__author__ = "Filip Salomonsson (filip@infix.se)"
__version__ = "0.1a"
__date__ = "2005-01-03"
__copyright__ = "Copyright (c) 2005 Filip Salomonsson \
liksom fan alltsa"
__license__ = "python"

class Token:
    """Represent a token."""
    def __init__(self, type, string, start, end, line):
        self.type = type
        self.string = string
        self.start = start
        self.end = end
        self.line = line
    def __str__(self):
        return str(self.string)


class Formatter:
    """A formatter."""
    encodings = {}
    def _encode(self, s):
        """Encode s."""
        if self.encodings:
            return "".join(map(self.encodings.get, s, s))
        return s

    def _default_format(self, token):
        return token.string

    def format(self, token):
        """Return a formatted representation of token."""
        handler = "format_%s" % str(tok_name.get(token.type)).lower()
        token.string = self._encode(token.string)
        return getattr(self, handler, self._default_format)(token)

class XMLFormatter(Formatter):
    def _default_format(self, token):
        return "[%s]%s" % (tok_name[token.type].lower(), token.string)
    def format_nl(self, token):
        return self._default_format(token) + "\n"

class LaTeXFormatter(Formatter):
    encodings = {
        '\n': r'\\' '\n',
        '"': r'\char"22 ',
        ' ': r'~',
        '#': r'\char"23 ',
        '$': r'\textdollar',
        '%': r'\char"25 ',
        '&': r'\char"26 ',
        "'": r'\char"27 ',
        '\\': r'\textbackslash ',
        '^': r'\textasciicircum',
        '_': r'\textunderscore ',
        '`': r'\char"60 ',
        '{': r'\textbraceleft ',
        '|': r'\textbar',
        '}': r'\textbraceright ',
        '~': r'\textasciitilde',
        '\xa0': r'~',
        '\xa1': r'\textexclamdown',
        '\xa3': r'\textsterling',
        '\xa7': r'\char"9F ',
        '\xa8': r'\char"04 ',
        '\xa9': r'\copyright',
        '\xab': r'\char"13 ',
        '\xac': r'$\neg$',
        '\xaf': r'\char"09 ',
        '\xb1': r'$\pm$',
        '\xb2': r'$^{2}$',
        '\xb3': r'$^{3}$',
        '\xb4': r'\char"01 ',
        '\xb5': r'$\mu$',
        '\xb8': r'\char"0D ',
        '\xb9': r'$^{1}$',
        '\xbb': r'\char"14 ',
        '\xbc': r'\mbox{$^{1}$\char"2F$_{4}$}',
        '\xbd': r'\mbox{$^{1}$\char"2F$_{2}$}',
        '\xbe': r'\mbox{$^{3}$\char"2F$_{4}$}',
        '\xbf': r'\textquestiondown',
        '\xc0': r'\`{A}',
        '\xc1': r'\'{A}',
        '\xc2': r'\^{A}',
        '\xc3': r'\~{A}',
        '\xc4': r'\"{A}',
        '\xc5': r'\AA',
        '\xc6': r'\AE',
        '\xc7': r'\c{C}',
        '\xc8': r'\`{E}',
        '\xc9': r'\'{E}',
        '\xca': r'\^{E}',
        '\xcb': r'\"{E}',
        '\xcc': r'\`{I}',
        '\xcd': r'\'{I}',
        '\xce': r'\^{I}',
        '\xcf': r'\"{I}',
        '\xd0': r'\DH',
        '\xd1': r'\~{N}',
        '\xd2': r'\`{O}',
        '\xd3': r'\'{O}',
        '\xd4': r'\^{O}',
        '\xd5': r'\~{O}',
        '\xd6': r'\"{O}',
        '\xd7': r'$\times$',
        '\xd8': r'\O',
        '\xd9': r'\`{U}',
        '\xda': r'\'{U}',
        '\xdb': r'\^{U}',
        '\xdc': r'\"{U}',
        '\xdd': r'\`{y}',
        '\xde': r'\TH',
        '\xdf': r'\ss',
        '\xe0': r'\`{a}',
        '\xe1': r'\'{a}',
        '\xe2': r'\^{a}',
        '\xe3': r'\~{a}',
        '\xe4': r'\"{a}',
        '\xe5': r'\aa',
        '\xe6': r'\ae',
        '\xe7': r'\c{c}',
        '\xe8': r'\`{e}',
        '\xe9': r'\'{e}',
        '\xea': r'\^{e}',
        '\xeb': r'\"{e}',
        '\xec': r'\`{\i}',
        '\xed': r'\'{\i}',
        '\xee': r'\^{\i}',
        '\xef': r'\"{\i}',
        '\xf0': r'\dh',
        '\xf1': r'\~{n}',
        '\xf2': r'\`{o}',
        '\xf3': r'\'{o}',
        '\xf4': r'\^{o}',
        '\xf5': r'\~{o}',
        '\xf6': r'\"{o}',
        '\xf7': r'$\div$',
        '\xf8': r'\o',
        '\xf9': r'\`{u}',
        '\xfa': r'\'{u}',
        '\xfb': r'\^{u}',
        '\xfc': r'\"{u}',
        '\xfd': r'\'{y}',
        '\xfe': r'\th',
        '\xff': r'\"{y}'
        }
#    def format_newline(self, token):
#        return "\\\\%s" % token.string
#    format_nl = format_newline
    def format_name(self, token):
        return r'\textbf{%s}' % token.string
    def format_string(self, token):
        return r'\textit{%s}' % token.string

def prettyprint(source=sys.stdin, output=sys.stdout, formatter=None):
    formatter = formatter or Formatter()
    format = formatter.format

    lastend = (0, 0)
    for token_tuple in tokenize.generate_tokens(source.readline):
        token = Token(*token_tuple)

        if token.start != lastend:
            output.write(formatter._encode(token.line[lastend[1]:token.start[1]]))

        output.write(format(token))
        lastend = token.end
        if lastend[1] == len(token.line):
            lastend = (token.end[0] + 1, 0)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        prettyprint(open(sys.argv[1]))
    else:
        prettyprint(formatter=LaTeXFormatter())

