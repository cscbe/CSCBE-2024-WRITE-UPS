#!/usr/bin/env python

from __future__ import print_function

__description__ = 'Case Connemara decoder'
__author__ = 'Didier Stevens'
__version__ = '0.0.1'
__date__ = '2023/09/22'

"""
Copyright NVISO 2023
Use at your own risk

History:
  2023/09/20: start
  2023/09/22: logging, DWG
  2024/02/07 added METADATATYPE_ALGO2

Todo:
  Document flag arguments in man page
"""

import optparse
import sys
import os
import binascii
import random
import gzip
import collections
import glob
import textwrap
import re
import struct
import string
import math
import fnmatch
import json
import time
import csv
try:
    import pyzipper as zipfile
except ImportError:
    import zipfile
import hashlib
if sys.version_info[0] >= 3:
    from io import BytesIO as DataIO
else:
    from cStringIO import StringIO as DataIO
if sys.version_info[0] >= 3:
    from io import StringIO
else:
    from cStringIO import StringIO

def PrintManual():
    manual = r'''
Manual:

Run this tool with one argument: the folder with files to be decrypted.

'''
    for line in manual.split('\n'):
        print(textwrap.fill(line, 79))

DEFAULT_SEPARATOR = ','
QUOTE = '"'

def PrintError(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

#Convert 2 Bytes If Python 3
def C2BIP3(string):
    if sys.version_info[0] > 2:
        return bytes([ord(x) for x in string])
    else:
        return string

#Convert 2 Integer If Python 2
def C2IIP2(data):
    if sys.version_info[0] > 2:
        return data
    else:
        return ord(data)

# CIC: Call If Callable
def CIC(expression):
    if callable(expression):
        return expression()
    else:
        return expression

# IFF: IF Function
def IFF(expression, valueTrue, valueFalse):
    if expression:
        return CIC(valueTrue)
    else:
        return CIC(valueFalse)

#-BEGINCODE cBinaryFile------------------------------------------------------------------------------
#import random
#import binascii
#import zipfile
#import gzip
#import sys
#if sys.version_info[0] >= 3:
#    from io import BytesIO as DataIO
#else:
#    from cStringIO import StringIO as DataIO

def LoremIpsumSentence(minimum, maximum):
    words = ['lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit', 'etiam', 'tortor', 'metus', 'cursus', 'sed', 'sollicitudin', 'ac', 'sagittis', 'eget', 'massa', 'praesent', 'sem', 'fermentum', 'dignissim', 'in', 'vel', 'augue', 'scelerisque', 'auctor', 'libero', 'nam', 'a', 'gravida', 'odio', 'duis', 'vestibulum', 'vulputate', 'quam', 'nec', 'cras', 'nibh', 'feugiat', 'ut', 'vitae', 'ornare', 'justo', 'orci', 'varius', 'natoque', 'penatibus', 'et', 'magnis', 'dis', 'parturient', 'montes', 'nascetur', 'ridiculus', 'mus', 'curabitur', 'nisl', 'egestas', 'urna', 'iaculis', 'lectus', 'maecenas', 'ultrices', 'velit', 'eu', 'porta', 'hac', 'habitasse', 'platea', 'dictumst', 'integer', 'id', 'commodo', 'mauris', 'interdum', 'malesuada', 'fames', 'ante', 'primis', 'faucibus', 'accumsan', 'pharetra', 'aliquam', 'nunc', 'at', 'est', 'non', 'leo', 'nulla', 'sodales', 'porttitor', 'facilisis', 'aenean', 'condimentum', 'rutrum', 'facilisi', 'tincidunt', 'laoreet', 'ultricies', 'neque', 'diam', 'euismod', 'consequat', 'tempor', 'elementum', 'lobortis', 'erat', 'ligula', 'risus', 'donec', 'phasellus', 'quisque', 'vivamus', 'pellentesque', 'tristique', 'venenatis', 'purus', 'mi', 'dictum', 'posuere', 'fringilla', 'quis', 'magna', 'pretium', 'felis', 'pulvinar', 'lacinia', 'proin', 'viverra', 'lacus', 'suscipit', 'aliquet', 'dui', 'molestie', 'dapibus', 'mollis', 'suspendisse', 'sapien', 'blandit', 'morbi', 'tellus', 'enim', 'maximus', 'semper', 'arcu', 'bibendum', 'convallis', 'hendrerit', 'imperdiet', 'finibus', 'fusce', 'congue', 'ullamcorper', 'placerat', 'nullam', 'eros', 'habitant', 'senectus', 'netus', 'turpis', 'luctus', 'volutpat', 'rhoncus', 'mattis', 'nisi', 'ex', 'tempus', 'eleifend', 'vehicula', 'class', 'aptent', 'taciti', 'sociosqu', 'ad', 'litora', 'torquent', 'per', 'conubia', 'nostra', 'inceptos', 'himenaeos']
    sample = random.sample(words, random.randint(minimum, maximum))
    sample[0] = sample[0].capitalize()
    return ' '.join(sample) + '.'

def LoremIpsum(sentences):
    return ' '.join([LoremIpsumSentence(15, 30) for i in range(sentences)])

STATE_START = 0
STATE_IDENTIFIER = 1
STATE_STRING = 2
STATE_SPECIAL_CHAR = 3
STATE_ERROR = 4

FUNCTIONNAME_REPEAT = 'repeat'
FUNCTIONNAME_RANDOM = 'random'
FUNCTIONNAME_CHR = 'chr'
FUNCTIONNAME_LOREMIPSUM = 'loremipsum'

def Tokenize(expression):
    result = []
    token = ''
    state = STATE_START
    while expression != '':
        char = expression[0]
        expression = expression[1:]
        if char == "'":
            if state == STATE_START:
                state = STATE_STRING
            elif state == STATE_IDENTIFIER:
                result.append([STATE_IDENTIFIER, token])
                state = STATE_STRING
                token = ''
            elif state == STATE_STRING:
                result.append([STATE_STRING, token])
                state = STATE_START
                token = ''
        elif char >= '0' and char <= '9' or char.lower() >= 'a' and char.lower() <= 'z':
            if state == STATE_START:
                token = char
                state = STATE_IDENTIFIER
            else:
                token += char
        elif char == ' ':
            if state == STATE_IDENTIFIER:
                result.append([STATE_IDENTIFIER, token])
                token = ''
                state = STATE_START
            elif state == STATE_STRING:
                token += char
        else:
            if state == STATE_IDENTIFIER:
                result.append([STATE_IDENTIFIER, token])
                token = ''
                state = STATE_START
                result.append([STATE_SPECIAL_CHAR, char])
            elif state == STATE_STRING:
                token += char
            else:
                result.append([STATE_SPECIAL_CHAR, char])
                token = ''
    if state == STATE_IDENTIFIER:
        result.append([state, token])
    elif state == STATE_STRING:
        result = [[STATE_ERROR, 'Error: string not closed', token]]
    return result

def ParseFunction(tokens):
    if len(tokens) == 0:
        print('Parsing error')
        return None, tokens
    if tokens[0][0] == STATE_STRING or tokens[0][0] == STATE_IDENTIFIER and tokens[0][1].startswith('0x'):
        return [[FUNCTIONNAME_REPEAT, [[STATE_IDENTIFIER, '1'], tokens[0]]], tokens[1:]]
    if tokens[0][0] != STATE_IDENTIFIER:
        print('Parsing error')
        return None, tokens
    function = tokens[0][1]
    tokens = tokens[1:]
    if len(tokens) == 0:
        print('Parsing error')
        return None, tokens
    if tokens[0][0] != STATE_SPECIAL_CHAR or tokens[0][1] != '(':
        print('Parsing error')
        return None, tokens
    tokens = tokens[1:]
    if len(tokens) == 0:
        print('Parsing error')
        return None, tokens
    arguments = []
    while True:
        if tokens[0][0] != STATE_IDENTIFIER and tokens[0][0] != STATE_STRING:
            print('Parsing error')
            return None, tokens
        arguments.append(tokens[0])
        tokens = tokens[1:]
        if len(tokens) == 0:
            print('Parsing error')
            return None, tokens
        if tokens[0][0] != STATE_SPECIAL_CHAR or (tokens[0][1] != ',' and tokens[0][1] != ')'):
            print('Parsing error')
            return None, tokens
        if tokens[0][0] == STATE_SPECIAL_CHAR and tokens[0][1] == ')':
            tokens = tokens[1:]
            break
        tokens = tokens[1:]
        if len(tokens) == 0:
            print('Parsing error')
            return None, tokens
    return [[function, arguments], tokens]

def Parse(expression):
    tokens = Tokenize(expression)
    if len(tokens) == 0:
        print('Parsing error')
        return None
    if tokens[0][0] == STATE_ERROR:
        print(tokens[0][1])
        print(tokens[0][2])
        print(expression)
        return None
    functioncalls = []
    while True:
        functioncall, tokens = ParseFunction(tokens)
        if functioncall == None:
            return None
        functioncalls.append(functioncall)
        if len(tokens) == 0:
            return functioncalls
        if tokens[0][0] != STATE_SPECIAL_CHAR or tokens[0][1] != '+':
            print('Parsing error')
            return None
        tokens = tokens[1:]

def InterpretInteger(token):
    if token[0] != STATE_IDENTIFIER:
        return None
    try:
        return int(token[1])
    except:
        return None

def Hex2Bytes(hexadecimal):
    if len(hexadecimal) % 2 == 1:
        hexadecimal = '0' + hexadecimal
    try:
        return binascii.a2b_hex(hexadecimal)
    except:
        return None

def InterpretHexInteger(token):
    if token[0] != STATE_IDENTIFIER:
        return None
    if not token[1].startswith('0x'):
        return None
    bytes = Hex2Bytes(token[1][2:])
    if bytes == None:
        return None
    integer = 0
    for byte in bytes:
        integer = integer * 0x100 + C2IIP2(byte)
    return integer

def InterpretNumber(token):
    number = InterpretInteger(token)
    if number == None:
        return InterpretHexInteger(token)
    else:
        return number

def InterpretBytes(token):
    if token[0] == STATE_STRING:
        return token[1]
    if token[0] != STATE_IDENTIFIER:
        return None
    if not token[1].startswith('0x'):
        return None
    return Hex2Bytes(token[1][2:])

def CheckFunction(functionname, arguments, countarguments, maxcountarguments=None):
    if maxcountarguments == None:
        if countarguments == 0 and len(arguments) != 0:
            print('Error: function %s takes no arguments, %d are given' % (functionname, len(arguments)))
            return True
        if countarguments == 1 and len(arguments) != 1:
            print('Error: function %s takes 1 argument, %d are given' % (functionname, len(arguments)))
            return True
        if countarguments != len(arguments):
            print('Error: function %s takes %d arguments, %d are given' % (functionname, countarguments, len(arguments)))
            return True
    else:
        if len(arguments) < countarguments or len(arguments) > maxcountarguments:
            print('Error: function %s takes between %d and %d arguments, %d are given' % (functionname, countarguments, maxcountarguments, len(arguments)))
            return True
    return False

def CheckNumber(argument, minimum=None, maximum=None):
    number = InterpretNumber(argument)
    if number == None:
        print('Error: argument should be a number: %s' % argument[1])
        return None
    if minimum != None and number < minimum:
        print('Error: argument should be minimum %d: %d' % (minimum, number))
        return None
    if maximum != None and number > maximum:
        print('Error: argument should be maximum %d: %d' % (maximum, number))
        return None
    return number

def Interpret(expression):
    functioncalls = Parse(expression)
    if functioncalls == None:
        return None
    decoded = ''
    for functioncall in functioncalls:
        functionname, arguments = functioncall
        if functionname == FUNCTIONNAME_REPEAT:
            if CheckFunction(functionname, arguments, 2):
                return None
            number = CheckNumber(arguments[0], minimum=1)
            if number == None:
                return None
            bytes = InterpretBytes(arguments[1])
            if bytes == None:
                print('Error: argument should be a byte sequence: %s' % arguments[1][1])
                return None
            decoded += number * bytes.decode('latin')
        elif functionname == FUNCTIONNAME_RANDOM:
            if CheckFunction(functionname, arguments, 1):
                return None
            number = CheckNumber(arguments[0], minimum=1)
            if number == None:
                return None
            decoded += ''.join([chr(random.randint(0, 255)) for x in range(number)])
        elif functionname == FUNCTIONNAME_LOREMIPSUM:
            if CheckFunction(functionname, arguments, 1):
                return None
            number = CheckNumber(arguments[0], minimum=1)
            if number == None:
                return None
            decoded += LoremIpsum(number)
        elif functionname == FUNCTIONNAME_CHR:
            if CheckFunction(functionname, arguments, 1, 2):
                return None
            number = CheckNumber(arguments[0], minimum=0, maximum=255)
            if number == None:
                return None
            if len(arguments) == 1:
                decoded += chr(number)
            else:
                number2 = CheckNumber(arguments[1], minimum=0, maximum=255)
                if number2 == None:
                    return None
                if number < number2:
                    decoded += ''.join([chr(n) for n in range(number, number2 + 1)])
                else:
                    decoded += ''.join([chr(n) for n in range(number, number2 - 1, -1)])
        else:
            print('Error: unknown function: %s' % functionname)
            return None
    return decoded

def ParsePackExpression(data):
    try:
        packFormat, pythonExpression = data.split('#', 1)
        data = struct.pack(packFormat, int(pythonExpression))
        return data
    except:
        return None

FCH_FILENAME = 0
FCH_DATA = 1
FCH_ERROR = 2

def FilenameCheckHash(filename, literalfilename):
    if literalfilename:
        return FCH_FILENAME, filename
    elif filename.startswith('#h#'):
        result = Hex2Bytes(filename[3:].replace(' ', ''))
        if result == None:
            return FCH_ERROR, 'hexadecimal'
        else:
            return FCH_DATA, result
    elif filename.startswith('#b#'):
        try:
            return FCH_DATA, binascii.a2b_base64(filename[3:])
        except:
            return FCH_ERROR, 'base64'
    elif filename.startswith('#e#'):
        result = Interpret(filename[3:])
        if result == None:
            return FCH_ERROR, 'expression'
        else:
            return FCH_DATA, C2BIP3(result)
    elif filename.startswith('#p#'):
        result = ParsePackExpression(filename[3:])
        if result == None:
            return FCH_ERROR, 'pack'
        else:
            return FCH_DATA, result
    elif filename.startswith('#'):
        return FCH_DATA, C2BIP3(filename[1:])
    else:
        return FCH_FILENAME, filename

def AnalyzeFileError(filename):
    PrintError('Error opening file %s' % filename)
    PrintError(sys.exc_info()[1])
    try:
        if not os.path.exists(filename):
            PrintError('The file does not exist')
        elif os.path.isdir(filename):
            PrintError('The file is a directory')
        elif not os.path.isfile(filename):
            PrintError('The file is not a regular file')
    except:
        pass

def CreateZipFileObject(arg1, arg2):
    if 'AESZipFile' in dir(zipfile):
        return zipfile.AESZipFile(arg1, arg2)
    else:
        return zipfile.ZipFile(arg1, arg2)

class cBinaryFile:
    def __init__(self, filename, zippassword='infected', noextraction=False, literalfilename=False):
        self.filename = filename
        self.zippassword = zippassword
        self.noextraction = noextraction
        self.literalfilename = literalfilename
        self.oZipfile = None
        self.extracted = False
        self.fIn = None

        fch, data = FilenameCheckHash(self.filename, self.literalfilename)
        if fch == FCH_ERROR:
            line = 'Error %s parsing filename: %s' % (data, self.filename)
            raise Exception(line)

        try:
            if self.filename == '':
                if sys.platform == 'win32':
                    import msvcrt
                    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
                self.fIn = sys.stdin
            elif fch == FCH_DATA:
                self.fIn = DataIO(data)
            elif not self.noextraction and self.filename.lower().endswith('.zip'):
                self.oZipfile = CreateZipFileObject(self.filename, 'r')
                if len(self.oZipfile.infolist()) == 1:
                    self.fIn = self.oZipfile.open(self.oZipfile.infolist()[0], 'r', self.zippassword)
                    self.extracted = True
                else:
                    self.oZipfile.close()
                    self.oZipfile = None
                    self.fIn = open(self.filename, 'rb')
            elif not self.noextraction and self.filename.lower().endswith('.gz'):
                self.fIn = gzip.GzipFile(self.filename, 'rb')
                self.extracted = True
            else:
                self.fIn = open(self.filename, 'rb')
        except:
            AnalyzeFileError(self.filename)
            raise

    def close(self):
        if self.fIn != sys.stdin and self.fIn != None:
            self.fIn.close()
        if self.oZipfile != None:
            self.oZipfile.close()

    def read(self, size=None):
        try:
            fRead = self.fIn.buffer
        except:
            fRead = self.fIn
        if size == None:
            return fRead.read()
        else:
            return fRead.read(size)

    def Data(self):
        data = self.read()
        self.close()
        return data

#-ENDCODE cBinaryFile--------------------------------------------------------------------------------

def File2Strings(filename):
    try:
        if filename == '':
            f = sys.stdin
        else:
            f = open(filename, 'r')
    except:
        return None
    try:
        return map(lambda line:line.rstrip('\n'), f.readlines())
    except:
        return None
    finally:
        if f != sys.stdin:
            f.close()

def File2String(filename):
    try:
        f = open(filename, 'rb')
    except:
        return None
    try:
        return f.read()
    except:
        return None
    finally:
        f.close()

def ProcessAt(argument):
    if argument.startswith('@'):
        strings = File2Strings(argument[1:])
        if strings == None:
            raise Exception('Error reading %s' % argument)
        else:
            return strings
    else:
        return [argument]

def Glob(filename):
    filenames = glob.glob(filename)
    if len(filenames) == 0:
        return [filename]
    else:
        return filenames

class cExpandFilenameArguments():
    def __init__(self, filenames, literalfilenames=False, recursedir=False, checkfilenames=False, expressionprefix=None, flagprefix=None):
        self.containsUnixShellStyleWildcards = False
        self.warning = False
        self.message = ''
        self.filenameexpressionsflags = []
        self.expressionprefix = expressionprefix
        self.flagprefix = flagprefix
        self.literalfilenames = literalfilenames

        expression = ''
        flag = ''
        if len(filenames) == 0:
            self.filenameexpressionsflags = [['', '', '']]
        elif literalfilenames:
            self.filenameexpressionsflags = [[filename, '', ''] for filename in filenames]
        elif recursedir:
            for dirwildcard in filenames:
                if expressionprefix != None and dirwildcard.startswith(expressionprefix):
                    expression = dirwildcard[len(expressionprefix):]
                elif flagprefix != None and dirwildcard.startswith(flagprefix):
                    flag = dirwildcard[len(flagprefix):]
                else:
                    if dirwildcard.startswith('@'):
                        for filename in ProcessAt(dirwildcard):
                            self.filenameexpressionsflags.append([filename, expression, flag])
                    elif os.path.isfile(dirwildcard):
                        self.filenameexpressionsflags.append([dirwildcard, expression, flag])
                    else:
                        if os.path.isdir(dirwildcard):
                            dirname = dirwildcard
                            basename = '*'
                        else:
                            dirname, basename = os.path.split(dirwildcard)
                            if dirname == '':
                                dirname = '.'
                        for path, dirs, files in os.walk(dirname):
                            for filename in fnmatch.filter(files, basename):
                                self.filenameexpressionsflags.append([os.path.join(path, filename), expression, flag])
        else:
            for filename in list(collections.OrderedDict.fromkeys(sum(map(self.Glob, sum(map(ProcessAt, filenames), [])), []))):
                if expressionprefix != None and filename.startswith(expressionprefix):
                    expression = filename[len(expressionprefix):]
                elif flagprefix != None and filename.startswith(flagprefix):
                    flag = filename[len(flagprefix):]
                else:
                    self.filenameexpressionsflags.append([filename, expression, flag])
            self.warning = self.containsUnixShellStyleWildcards and len(self.filenameexpressionsflags) == 0
            if self.warning:
                self.message = "Your filename argument(s) contain Unix shell-style wildcards, but no files were matched.\nCheck your wildcard patterns or use option literalfilenames if you don't want wildcard pattern matching."
                return
        if self.filenameexpressionsflags == [] and (expression != '' or flag != ''):
            self.filenameexpressionsflags = [['', expression, flag]]
        if checkfilenames:
            self.CheckIfFilesAreValid()

    def Glob(self, filename):
        if not ('?' in filename or '*' in filename or ('[' in filename and ']' in filename)):
            return [filename]
        self.containsUnixShellStyleWildcards = True
        return glob.glob(filename)

    def CheckIfFilesAreValid(self):
        valid = []
        doesnotexist = []
        isnotafile = []
        for filename, expression, flag in self.filenameexpressionsflags:
            hashfile = False
            try:
                hashfile = FilenameCheckHash(filename, self.literalfilenames)[0] == FCH_DATA
            except:
                pass
            if filename == '' or hashfile:
                valid.append([filename, expression, flag])
            elif not os.path.exists(filename):
                doesnotexist.append(filename)
            elif not os.path.isfile(filename):
                isnotafile.append(filename)
            else:
                valid.append([filename, expression, flag])
        self.filenameexpressionsflags = valid
        if len(doesnotexist) > 0:
            self.warning = True
            self.message += 'The following files do not exist and will be skipped: ' + ' '.join(doesnotexist) + '\n'
        if len(isnotafile) > 0:
            self.warning = True
            self.message += 'The following files are not regular files and will be skipped: ' + ' '.join(isnotafile) + '\n'

    def Filenames(self):
        if self.expressionprefix == None:
            return [filename for filename, expression, flag in self.filenameexpressionsflags]
        else:
            return self.filenameexpressionsflags

def CheckJSON(stringJSON):
    try:
        object = json.loads(stringJSON)
    except:
        print('Error parsing JSON')
        print(sys.exc_info()[1])
        return None
    if not isinstance(object, dict):
        print('Error JSON is not a dictionary')
        return None
    if not 'version' in object:
        print('Error JSON dictionary has no version')
        return None
    if object['version'] != 2:
        print('Error JSON dictionary has wrong version')
        return None
    if not 'id' in object:
        print('Error JSON dictionary has no id')
        return None
    if object['id'] != 'didierstevens.com':
        print('Error JSON dictionary has wrong id')
        return None
    if not 'type' in object:
        print('Error JSON dictionary has no type')
        return None
    if object['type'] != 'content':
        print('Error JSON dictionary has wrong type')
        return None
    if not 'fields' in object:
        print('Error JSON dictionary has no fields')
        return None
    if not 'name' in object['fields']:
        print('Error JSON dictionary has no name field')
        return None
    if not 'content' in object['fields']:
        print('Error JSON dictionary has no content field')
        return None
    if not 'items' in object:
        print('Error JSON dictionary has no items')
        return None
    for item in object['items']:
        item['content'] = binascii.a2b_base64(item['content'])
    return object['items']

CUTTERM_NOTHING = 0
CUTTERM_POSITION = 1
CUTTERM_FIND = 2
CUTTERM_LENGTH = 3

def Replace(string, dReplacements):
    if string in dReplacements:
        return dReplacements[string]
    else:
        return string

def ParseInteger(argument):
    sign = 1
    if argument.startswith('+'):
        argument = argument[1:]
    elif argument.startswith('-'):
        argument = argument[1:]
        sign = -1
    if argument.startswith('0x'):
        return sign * int(argument[2:], 16)
    else:
        return sign * int(argument)

def ParseCutTerm(argument):
    if argument == '':
        return CUTTERM_NOTHING, None, ''
    oMatch = re.match(r'\-?0x([0-9a-f]+)', argument, re.I)
    if oMatch == None:
        oMatch = re.match(r'\-?(\d+)', argument)
    else:
        value = int(oMatch.group(1), 16)
        if argument.startswith('-'):
            value = -value
        return CUTTERM_POSITION, value, argument[len(oMatch.group(0)):]
    if oMatch == None:
        oMatch = re.match(r'\[([0-9a-f]+)\](\d+)?([+-](?:0x[0-9a-f]+|\d+))?', argument, re.I)
    else:
        value = int(oMatch.group(1))
        if argument.startswith('-'):
            value = -value
        return CUTTERM_POSITION, value, argument[len(oMatch.group(0)):]
    if oMatch == None:
        oMatch = re.match(r"\[u?\'(.+?)\'\](\d+)?([+-](?:0x[0-9a-f]+|\d+))?", argument)
    else:
        if len(oMatch.group(1)) % 2 == 1:
            raise Exception("Uneven length hexadecimal string")
        else:
            return CUTTERM_FIND, (binascii.a2b_hex(oMatch.group(1)), int(Replace(oMatch.group(2), {None: '1'})), ParseInteger(Replace(oMatch.group(3), {None: '0'}))), argument[len(oMatch.group(0)):]
    if oMatch == None:
        return None, None, argument
    else:
        if argument.startswith("[u'"):
            # convert ascii to unicode 16 byte sequence
            searchtext = oMatch.group(1).encode('utf16')[2:]
        else:
            searchtext = oMatch.group(1).encode('latin')
        return CUTTERM_FIND, (searchtext, int(Replace(oMatch.group(2), {None: '1'})), ParseInteger(Replace(oMatch.group(3), {None: '0'}))), argument[len(oMatch.group(0)):]

def ParseCutArgument(argument):
    type, value, remainder = ParseCutTerm(argument.strip())
    if type == CUTTERM_NOTHING:
        return CUTTERM_NOTHING, None, CUTTERM_NOTHING, None
    elif type == None:
        if remainder.startswith(':'):
            typeLeft = CUTTERM_NOTHING
            valueLeft = None
            remainder = remainder[1:]
        else:
            return None, None, None, None
    else:
        typeLeft = type
        valueLeft = value
        if typeLeft == CUTTERM_POSITION and valueLeft < 0:
            return None, None, None, None
        if typeLeft == CUTTERM_FIND and valueLeft[1] == 0:
            return None, None, None, None
        if remainder.startswith(':'):
            remainder = remainder[1:]
        else:
            return None, None, None, None
    type, value, remainder = ParseCutTerm(remainder)
    if type == CUTTERM_POSITION and remainder == 'l':
        return typeLeft, valueLeft, CUTTERM_LENGTH, value
    elif type == None or remainder != '':
        return None, None, None, None
    elif type == CUTTERM_FIND and value[1] == 0:
        return None, None, None, None
    else:
        return typeLeft, valueLeft, type, value

def Find(data, value, nth, startposition=-1):
    position = startposition
    while nth > 0:
        position = data.find(value, position + 1)
        if position == -1:
            return -1
        nth -= 1
    return position

def CutData(stream, cutArgument):
    if cutArgument == '':
        return [stream, None, None]

    typeLeft, valueLeft, typeRight, valueRight = ParseCutArgument(cutArgument)

    if typeLeft == None:
        return [stream, None, None]

    if typeLeft == CUTTERM_NOTHING:
        positionBegin = 0
    elif typeLeft == CUTTERM_POSITION:
        positionBegin = valueLeft
    elif typeLeft == CUTTERM_FIND:
        positionBegin = Find(stream, valueLeft[0], valueLeft[1])
        if positionBegin == -1:
            return ['', None, None]
        positionBegin += valueLeft[2]
    else:
        raise Exception("Unknown value typeLeft")

    if typeRight == CUTTERM_NOTHING:
        positionEnd = len(stream)
    elif typeRight == CUTTERM_POSITION and valueRight < 0:
        positionEnd = len(stream) + valueRight
    elif typeRight == CUTTERM_POSITION:
        positionEnd = valueRight + 1
    elif typeRight == CUTTERM_LENGTH:
        positionEnd = positionBegin + valueRight
    elif typeRight == CUTTERM_FIND:
        positionEnd = Find(stream, valueRight[0], valueRight[1], positionBegin)
        if positionEnd == -1:
            return ['', None, None]
        else:
            positionEnd += len(valueRight[0])
        positionEnd += valueRight[2]
    else:
        raise Exception("Unknown value typeRight")

    return [stream[positionBegin:positionEnd], positionBegin, positionEnd]

#-BEGINCODE cDump------------------------------------------------------------------------------------
#import binascii
#import sys
#if sys.version_info[0] >= 3:
#    from io import StringIO
#else:
#    from cStringIO import StringIO

class cDump():
    def __init__(self, data, prefix='', offset=0, dumplinelength=16):
        self.data = data
        self.prefix = prefix
        self.offset = offset
        self.dumplinelength = dumplinelength

    def HexDump(self):
        oDumpStream = self.cDumpStream(self.prefix)
        hexDump = ''
        for i, b in enumerate(self.data):
            if i % self.dumplinelength == 0 and hexDump != '':
                oDumpStream.Addline(hexDump)
                hexDump = ''
            hexDump += IFF(hexDump == '', '', ' ') + '%02X' % self.C2IIP2(b)
        oDumpStream.Addline(hexDump)
        return oDumpStream.Content()

    def CombineHexAscii(self, hexDump, asciiDump):
        if hexDump == '':
            return ''
        countSpaces = 3 * (self.dumplinelength - len(asciiDump))
        if len(asciiDump) <= self.dumplinelength / 2:
            countSpaces += 1
        return hexDump + '  ' + (' ' * countSpaces) + asciiDump

    def HexAsciiDump(self, rle=False):
        oDumpStream = self.cDumpStream(self.prefix)
        position = ''
        hexDump = ''
        asciiDump = ''
        previousLine = None
        countRLE = 0
        for i, b in enumerate(self.data):
            b = self.C2IIP2(b)
            if i % self.dumplinelength == 0:
                if hexDump != '':
                    line = self.CombineHexAscii(hexDump, asciiDump)
                    if not rle or line != previousLine:
                        if countRLE > 0:
                            oDumpStream.Addline('* %d 0x%02x' % (countRLE, countRLE * self.dumplinelength))
                        oDumpStream.Addline(position + line)
                        countRLE = 0
                    else:
                        countRLE += 1
                    previousLine = line
                position = '%08X:' % (i + self.offset)
                hexDump = ''
                asciiDump = ''
            if i % self.dumplinelength == self.dumplinelength / 2:
                hexDump += ' '
            hexDump += ' %02X' % b
            asciiDump += IFF(b >= 32 and b < 127, chr(b), '.')
        if countRLE > 0:
            oDumpStream.Addline('* %d 0x%02x' % (countRLE, countRLE * self.dumplinelength))
        oDumpStream.Addline(self.CombineHexAscii(position + hexDump, asciiDump))
        return oDumpStream.Content()

    def Base64Dump(self, nowhitespace=False):
        encoded = binascii.b2a_base64(self.data).decode().strip()
        if nowhitespace:
            return encoded
        oDumpStream = self.cDumpStream(self.prefix)
        length = 64
        for i in range(0, len(encoded), length):
            oDumpStream.Addline(encoded[0+i:length+i])
        return oDumpStream.Content()

    def HexDumpNoWS(self):
        return self.data.hex()

    def DumpOption(self, option):
        if option == 'a':
            return self.HexAsciiDump()
        elif option == 'A':
            return self.HexAsciiDump(rle=True)
        elif option == 'x':
            return self.HexDump()
        elif option == 'X':
            return self.HexDumpNoWS()
        elif option == 'b':
            return self.Base64Dump()
        elif option == 'B':
            return self.Base64Dump(nowhitespace=True)
        else:
            raise Exception('DumpOption: unknown option %' % option)

    class cDumpStream():
        def __init__(self, prefix=''):
            self.oStringIO = StringIO()
            self.prefix = prefix

        def Addline(self, line):
            if line != '':
                self.oStringIO.write(self.prefix + line + '\n')

        def Content(self):
            return self.oStringIO.getvalue()

    @staticmethod
    def C2IIP2(data):
        if sys.version_info[0] > 2:
            return data
        else:
            return ord(data)
#-ENDCODE cDump--------------------------------------------------------------------------------------

def IfWIN32SetBinary(io):
    if sys.platform == 'win32':
        import msvcrt
        msvcrt.setmode(io.fileno(), os.O_BINARY)

#Fix for http://bugs.python.org/issue11395
def StdoutWriteChunked(data):
    if sys.version_info[0] > 2:
        if isinstance(data, str):
            sys.stdout.write(data)
        else:
            sys.stdout.buffer.write(data)
    else:
        while data != '':
            sys.stdout.write(data[0:10000])
            try:
                sys.stdout.flush()
            except IOError:
                return
            data = data[10000:]

class cVariables():
    def __init__(self, variablesstring='', separator=DEFAULT_SEPARATOR):
        self.dVariables = {}
        if variablesstring == '':
            return
        for variable in variablesstring.split(separator):
            name, value = VariableNameValue(variable)
            self.dVariables[name] = value

    def SetVariable(self, name, value):
        self.dVariables[name] = value

    def Instantiate(self, astring):
        for key, value in self.dVariables.items():
            astring = astring.replace('%' + key + '%', value)
        return astring

class cOutput():
    def __init__(self, filenameOption=None, binary=False):
        self.starttime = time.time()
        self.filenameOption = filenameOption
        self.separateFiles = False
        self.progress = False
        self.console = False
        self.head = False
        self.headCounter = 0
        self.tail = False
        self.tailQueue = []
        self.STDOUT = 'STDOUT'
        self.fOut = None
        self.oCsvWriter = None
        self.rootFilenames = {}
        self.binary = binary
        if self.binary:
            self.fileoptions = 'wb'
        else:
            self.fileoptions = 'w'
        self.dReplacements = {}

    def Replace(self, line):
        for key, value in self.dReplacements.items():
            line = line.replace(key, value)
        return line

    def Open(self, binary=False):
        if self.fOut != None:
            return

        if binary:
            self.fileoptions = 'wb'
        else:
            self.fileoptions = 'w'

        if self.filenameOption:
            if self.ParseHash(self.filenameOption):
                if not self.separateFiles and self.filename != '':
                    self.fOut = open(self.filename, self.fileoptions, encoding='utf8', errors='ignore')
            elif self.filenameOption != '':
                self.fOut = open(self.filenameOption, self.fileoptions, encoding='utf8', errors='ignore')
        else:
            self.fOut = self.STDOUT

    def ParseHash(self, option):
        if option.startswith('#'):
            position = self.filenameOption.find('#', 1)
            if position > 1:
                switches = self.filenameOption[1:position]
                self.filename = self.filenameOption[position + 1:]
                for switch in switches:
                    if switch == 's':
                        self.separateFiles = True
                    elif switch == 'p':
                        self.progress = True
                    elif switch == 'c':
                        self.console = True
                    elif switch == 'l':
                        pass
                    elif switch == 'g':
                        if self.filename != '':
                            extra = self.filename + '-'
                        else:
                            extra = ''
                        self.filename = '%s-%s%s.txt' % (os.path.splitext(os.path.basename(sys.argv[0]))[0], extra, self.FormatTime())
                    elif switch == 'h':
                        self.head = True
                    elif switch == 't':
                        self.tail = True
                    else:
                        return False
                return True
        return False

    @staticmethod
    def FormatTime(epoch=None):
        if epoch == None:
            epoch = time.time()
        return '%04d%02d%02d-%02d%02d%02d' % time.localtime(epoch)[0:6]

    def RootUnique(self, root):
        if not root in self.rootFilenames:
            self.rootFilenames[root] = None
            return root
        iter = 1
        while True:
            newroot = '%s_%04d' % (root, iter)
            if not newroot in self.rootFilenames:
                self.rootFilenames[newroot] = None
                return newroot
            iter += 1

    def LineSub(self, line, eol):
        line = self.Replace(line)
        self.Open()
        if self.fOut == self.STDOUT or self.console:
            try:
                print(line, end=eol)
            except UnicodeEncodeError:
                encoding = sys.stdout.encoding
                print(line.encode(encoding, errors='backslashreplace').decode(encoding), end=eol)
#            sys.stdout.flush()
        if self.fOut != self.STDOUT:
            self.fOut.write(line + '\n')
            self.fOut.flush()

    def Line(self, line, eol='\n'):
        if self.head:
            if self.headCounter < 10:
                self.LineSub(line, eol)
            elif self.tail:
                self.tailQueue = self.tailQueue[-9:] + [[line, eol]]
            self.headCounter += 1
        elif self.tail:
            self.tailQueue = self.tailQueue[-9:] + [[line, eol]]
        else:
            self.LineSub(line, eol)

    def LineTimestamped(self, line):
        self.Line('%s: %s' % (self.FormatTime(), line))

    def WriteBinary(self, data):
        self.Open(True)
        if self.fOut != self.STDOUT:
            self.fOut.write(data)
            self.fOut.flush()
        else:
            IfWIN32SetBinary(sys.stdout)
            StdoutWriteChunked(data)

    def CSVWriteRow(self, row):
        if self.oCsvWriter == None:
            self.StringIOCSV = StringIO()
#            self.oCsvWriter = csv.writer(self.fOut)
            self.oCsvWriter = csv.writer(self.StringIOCSV)
        self.oCsvWriter.writerow(row)
        self.Line(self.StringIOCSV.getvalue(), '')
        self.StringIOCSV.truncate(0)
        self.StringIOCSV.seek(0)

    def Filename(self, filename, index, total):
        self.separateFilename = filename
        if self.progress:
            if index == 0:
                eta = ''
            else:
                seconds = int(float((time.time() - self.starttime) / float(index)) * float(total - index))
                eta = 'estimation %d seconds left, finished %s ' % (seconds, self.FormatTime(time.time() + seconds))
            PrintError('%d/%d %s%s' % (index + 1, total, eta, self.separateFilename))
        if self.separateFiles and self.filename != '':
            oFilenameVariables = cVariables()
            oFilenameVariables.SetVariable('f', self.separateFilename)
            basename = os.path.basename(self.separateFilename)
            oFilenameVariables.SetVariable('b', basename)
            oFilenameVariables.SetVariable('d', os.path.dirname(self.separateFilename))
            root, extension = os.path.splitext(basename)
            oFilenameVariables.SetVariable('r', root)
            oFilenameVariables.SetVariable('ru', self.RootUnique(root))
            oFilenameVariables.SetVariable('e', extension)

            self.Close()
            self.fOut = open(oFilenameVariables.Instantiate(self.filename), self.fileoptions)

    def Close(self):
        if self.head and self.tail and len(self.tailQueue) > 0:
            self.LineSub('...', '\n')

        for line, eol in self.tailQueue:
            self.LineSub(line, eol)

        self.headCounter = 0
        self.tailQueue = []

        if self.fOut != self.STDOUT:
            self.fOut.close()
            self.fOut = None

def ToString(value):
    if isinstance(value, str):
        return value
    else:
        return str(value)

def Quote(value, separator, quote):
    value = ToString(value)
    if len(value) > 1 and value[0] == quote and value[-1] == quote:
        return value
    if separator in value or value == '':
        return quote + value + quote
    else:
        return value

def MakeCSVLine(row, separator, quote):
    return separator.join([Quote(value, separator, quote) for value in row])

class cLogfile():
    def __init__(self, keyword, comment):
        self.starttime = time.time()
        self.errors = 0
        if keyword == '':
            self.oOutput = None
        else:
            self.oOutput = cOutput('%s-%s-%s.log' % (os.path.splitext(os.path.basename(sys.argv[0]))[0], keyword, self.FormatTime()))
        self.counter1 = 0
        self.counter2 = 0
        self.Line('Start')
        self.Line('UTC', '%04d%02d%02d-%02d%02d%02d' % time.gmtime(time.time())[0:6])
        self.Line('Comment', comment)
        self.Line('Args', repr(sys.argv))
        self.Line('Version', __version__)
        self.Line('Python', repr(sys.version_info))
        self.Line('Platform', sys.platform)
        self.Line('CWD', repr(os.getcwd()))

    @staticmethod
    def FormatTime(epoch=None):
        if epoch == None:
            epoch = time.time()
        return '%04d%02d%02d-%02d%02d%02d' % time.localtime(epoch)[0:6]

    def Line(self, *line):
        if self.oOutput != None:
            self.counter1 += 1
            csvline = MakeCSVLine((self.FormatTime(), ) + line, DEFAULT_SEPARATOR, QUOTE)
            self.counter2 += len(csvline)
            self.oOutput.Line(csvline)

    def LineError(self, *line):
        self.Line('Error', *line)
        self.errors += 1

    def Close(self):
        if self.oOutput != None:
            self.Line('Finish', '%d error(s)' % self.errors, '%d second(s)' % (time.time() - self.starttime), self.counter1, self.counter2)
            self.oOutput.Close()

def CalculateByteStatistics(dPrevalence=None, data=None):
    longestString = 0
    longestBASE64String = 0
    longestHEXString = 0
    base64digits = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/'
    hexdigits = b'abcdefABCDEF0123456789'
    averageConsecutiveByteDifference = None
    if dPrevalence == None:
        dPrevalence = {iter: 0 for iter in range(0x100)}
        sumDifferences = 0.0
        previous = None
        if len(data) > 1:
            lengthString = 0
            lengthBASE64String = 0
            lengthHEXString = 0
            for byte in data:
                byte = C2IIP2(byte)
                dPrevalence[byte] += 1
                if previous != None:
                    sumDifferences += abs(byte - previous)
                    if byte >= 0x20 and byte < 0x7F:
                        lengthString += 1
                    else:
                        longestString = max(longestString, lengthString)
                        lengthString = 0
                    if byte in base64digits:
                        lengthBASE64String += 1
                    else:
                        longestBASE64String = max(longestBASE64String, lengthBASE64String)
                        lengthBASE64String = 0
                    if byte in hexdigits:
                        lengthHEXString += 1
                    else:
                        longestHEXString = max(longestHEXString, lengthHEXString)
                        lengthHEXString = 0
                else:
                    if byte >= 0x20 and byte < 0x7F:
                        lengthString = 1
                    if byte in hexdigits:
                        lengthHEXString = 1
                previous = byte
            averageConsecutiveByteDifference = sumDifferences /float(len(data)-1)
            longestString = max(longestString, lengthString)
            longestBASE64String = max(longestBASE64String, lengthBASE64String)
            longestHEXString = max(longestHEXString, lengthHEXString)
    sumValues = sum(dPrevalence.values())
    countNullByte = dPrevalence[0]
    countControlBytes = 0
    countWhitespaceBytes = 0
    countUniqueBytes = 0
    for iter in range(1, 0x21):
        if chr(iter) in string.whitespace:
            countWhitespaceBytes += dPrevalence[iter]
        else:
            countControlBytes += dPrevalence[iter]
    countControlBytes += dPrevalence[0x7F]
    countPrintableBytes = 0
    for iter in range(0x21, 0x7F):
        countPrintableBytes += dPrevalence[iter]
    countHighBytes = 0
    for iter in range(0x80, 0x100):
        countHighBytes += dPrevalence[iter]
    countHexadecimalBytes = 0
    countBASE64Bytes = 0
    for iter in range(0x30, 0x3A):
        countHexadecimalBytes += dPrevalence[iter]
        countBASE64Bytes += dPrevalence[iter]
    for iter in range(0x41, 0x47):
        countHexadecimalBytes += dPrevalence[iter]
    for iter in range(0x61, 0x67):
        countHexadecimalBytes += dPrevalence[iter]
    for iter in range(0x41, 0x5B):
        countBASE64Bytes += dPrevalence[iter]
    for iter in range(0x61, 0x7B):
        countBASE64Bytes += dPrevalence[iter]
    countBASE64Bytes += dPrevalence[ord('+')] + dPrevalence[ord('/')] + dPrevalence[ord('=')]
    entropy = 0.0
    for iter in range(0x100):
        if dPrevalence[iter] > 0:
            prevalence = float(dPrevalence[iter]) / float(sumValues)
            entropy += - prevalence * math.log(prevalence, 2)
            countUniqueBytes += 1
    if sumValues >= 256:
        entropymax = 8.0
        entropynormalized = entropy
        entropystr = '%.02f' % entropy
    else:
        entropymax = math.log(sumValues, 2)
        entropynormalized = entropy / entropymax * 8.0
        entropystr = '%.02f (normalized %.02f max %.02f)' % (entropy, entropynormalized, entropymax)
    return sumValues, entropy, entropymax, entropystr, countUniqueBytes, countNullByte, countControlBytes, countWhitespaceBytes, countPrintableBytes, countHighBytes, countHexadecimalBytes, countBASE64Bytes, averageConsecutiveByteDifference, longestString, longestHEXString, longestBASE64String, dPrevalence

def CalculateByteStatisticsNT(dPrevalence=None, data=None):
    oNT = collections.namedtuple('bytestatistics', 'sumValues entropy entropymax entropystr countUniqueBytes countNullByte countControlBytes countWhitespaceBytes countPrintableBytes countHighBytes countHexadecimalBytes countBASE64Bytes averageConsecutiveByteDifference longestString longestHEXString longestBASE64String dPrevalence')
    return oNT(*CalculateByteStatistics(dPrevalence, data))

def Unpack(format, data):
    size = struct.calcsize(format)
    result = list(struct.unpack(format, data[:size]))
    result.append(data[size:])
    return result

def InstantiateCOutput(options):
    filenameOption = None
    if options.output != '':
        filenameOption = options.output
    binary = False
    if hasattr(options, 'dump'):
        binary = options.dump
    return cOutput(filenameOption, binary)

class cStruct(object):
    def __init__(self, data):
        self.data = data
        self.originaldata = data

    #a# extend z usage
    def UnpackSub(self, format):
        if format.endswith('z'):
            format = format[:-1]
            sz = True
        else:
            sz = False
        formatsize = struct.calcsize(format)
        if len(self.data) < formatsize:
            raise Exception('Not enough data')
        tounpack = self.data[:formatsize]
        self.data = self.data[formatsize:]
        result = struct.unpack(format, tounpack)
        if sz:
            result = result + (self.GetString0(), )
        return result

    def Unpack(self, format):
        result = self.UnpackSub(format)
        if len(result) == 1:
            return result[0]
        else:
            return result

    def UnpackNamedtuple(self, format, typename, field_names):
        namedTuple = collections.namedtuple(typename, field_names)
        result = self.UnpackSub(format)
        return namedTuple(*result)

    def Truncate(self, length):
        self.data = self.data[:length]

    def GetBytes(self, length=None):
        if length == None:
            length = len(self.data)
        result = self.data[:length]
        if len(result) < length:
            raise Exception('Not enough data')
        self.data = self.data[length:]
        return result

    def GetString(self, format):
        stringLength = self.Unpack(format)
        return self.GetBytes(stringLength)

    def Length(self):
        return len(self.data)

    def GetString0(self):
        position = self.data.find(b'\x00')
        if position == -1:
            raise Exception('Missing NUL byte')
        result = self.data[:position]
        self.data = self.data[position + 1:]
        return result

def FindAll(data, sub):
    result = []
    start = 0
    while True:
        position = data.find(sub, start)
        if position == -1:
            return result
        result.append(position)
        start = position + 1

def FormatTime(epoch=None):
    if epoch == None:
        epoch = time.time()
    return '%04d%02d%02d-%02d%02d%02d' % time.localtime(epoch)[0:6]

class cEnumeration(object):
    def __init__(self, iterable, function=lambda x: x, Cache=None):
        self.iterable = iterable
        self.function = function
        self.namedTuple = collections.namedtuple('member', 'item item_t index counter remaining total first last left left_t right right_t cached cache_hits cache_misses Cache Redo redo_counter remaining_seconds eta')
        self.flagRedo = False
        self.oCache = Cache
        self.cache_hits = 0
        self.cache_misses = 0
        self.timeStart = time.time()

    def __iter__(self):
        self.index = -1
        self.total = len(self.iterable)
        if self.oCache != None and self.oCache.cachedFirst:
            self.iterable = sorted(self.iterable, key=lambda x: not self.oCache.Exists(x))
        return self

    def Redo(self, counter):
        if self.nt.redo_counter < counter:
            self.nt = self.namedTuple(self.nt.item, self.nt.item_t, self.nt.index, self.nt.counter, self.nt.remaining, self.nt.total, self.nt.first, self.nt.last, self.nt.left, self.nt.left_t, self.nt.right, self.nt.right_t, self.nt.cached, self.nt.cache_hits, self.nt.cache_misses, self.nt.Cache, self.nt.Redo, self.nt.redo_counter + 1, self.nt.remaining_seconds, self.nt.eta)
            self.flagRedo = True
            return True
        else:
            self.flagRedo = False
            return False

    def Cache(self, result):
        if self.oCache == None:
            return False
        else:
            return self.oCache.Cache(self.nt.item, result, self.nt.last)

    def __next__(self):
        timeNow = time.time()
        if self.flagRedo:
            self.flagRedo = False
            return self.nt
        if self.index < self.total - 1:
            self.index += 1
            first = self.index == 0
            last = self.index == self.total - 1
            if first:
                left = None
                left_t = None
                self.item = self.iterable[self.index]
                self.item_t = self.function(self.item)
            else:
                left = self.item
                left_t = self.item_t
                self.item = self.right
                self.item_t = self.right_t
            if last:
                self.right = None
                self.right_t = None
            else:
                self.right = self.iterable[self.index + 1]
                self.right_t = self.function(self.right)
            if self.oCache == None:
                cachedResult = None
            else:
                cachedResult = self.oCache.Retrieve(self.item)
            if cachedResult == None:
                self.cache_misses += 1
            else:
                self.cache_hits += 1
            try:
                remainingSeconds = (self.total - self.index - 1) / (self.cache_misses / (timeNow - self.timeStart))
            except ZeroDivisionError:
                remainingSeconds = 0
            eta = FormatTime(time.time() + remainingSeconds)
            self.nt = self.namedTuple(self.item, self.item_t, self.index, self.index + 1, self.total - self.index - 1, self.total, first, last, left, left_t, self.right, self.right_t, cachedResult, self.cache_hits, self.cache_misses, self.Cache, self.Redo, 0, remainingSeconds, eta)
            return self.nt
        raise StopIteration

class cMagicValue(object):
    def __init__(self, data):
        self.data = data[:4]
        self.hexadecimal = binascii.b2a_hex(self.data).decode()
        self.printable = ''.join([chr(byte) if byte >= 32 and byte < 127 else '.' for byte in self.data])
        self.both = self.printable + ' ' + self.hexadecimal

class cHashCRC32():
    def __init__(self):
        self.crc32 = None

    def update(self, data):
        self.crc32 = zlib.crc32(data)

    def hexdigest(self):
        return '%08x' % (self.crc32 & 0xffffffff)

class cHashChecksum8():
    def __init__(self):
        self.sum = 0

    def update(self, data):
        if sys.version_info[0] >= 3:
            self.sum += sum(data)
        else:
            self.sum += sum(map(ord, data))

    def hexdigest(self):
        return '%08x' % (self.sum)

dSpecialHashes = {'crc32': cHashCRC32, 'checksum8': cHashChecksum8}

def GetHashObjects(algorithms):
    global dSpecialHashes

    dHashes = {}

    if algorithms == '':
        algorithms = os.getenv('DSS_DEFAULT_HASH_ALGORITHMS', 'md5')
    if ',' in algorithms:
        hashes = algorithms.split(',')
    else:
        hashes = algorithms.split(';')
    for name in hashes:
        if not name in dSpecialHashes.keys() and not name in hashlib.algorithms_available:
            print('Error: unknown hash algorithm: %s' % name)
            print('Available hash algorithms: ' + ' '.join([name for name in list(hashlib.algorithms_available)] + list(dSpecialHashes.keys())))
            return [], {}
        elif name in dSpecialHashes.keys():
            dHashes[name] = dSpecialHashes[name]()
        else:
            dHashes[name] = hashlib.new(name)

    return hashes, dHashes

def CalculateChosenHash(data):
    hashes, dHashes = GetHashObjects('')
    dHashes[hashes[0]].update(data)
    return dHashes[hashes[0]].hexdigest(), hashes[0]

def GetDumpOption(options, default=None):
    dPossibleOptions = {
        'asciidump': 'a',
        'hexdump': 'x',
        'dump': 'd',
        'asciidumprle': 'A',
        'hexdumpnows': 'X',
        'base64': 'b',
        'base64nows': 'B',
    }

    for attribute, option in dPossibleOptions.items():
        if hasattr(options, attribute) and getattr(options, attribute):
            return option
    return default

def DoDump(data, options, oOutput, default='a'):
    if hasattr(options, 'dump') and options.dump:
        oOutput.WriteBinary(data)
    else:
        oOutput.Line(cDump(data).DumpOption(GetDumpOption(options, default)))

# Copy as Python - from 010 Editor - byte count: 30000000 (0x1C9C380)
DECRYPTIONSTREAM = b''

def ExtraInfoHEADASCII(data):
    if data == None:
        return ''
    return ''.join([IFF(b >= 32 and b < 127, chr(b), '.') for b in data[:8]])

fileCounter = 0
fileStarttime = time.time()

def AlgoVersion1(length, numberofblocks=10):
    blocksize = int(length / (numberofblocks * 10)) & 0xFFFFFFFFF0
    stepsize = int(length / numberofblocks)
    return blocksize, stepsize, numberofblocks

def AlgoVersion2Sub(length, numberofblocks=10):
    blocksize = round(length / (numberofblocks * 10)) & 0xFFFFFFFFF0
    stepsize = int(length / numberofblocks)
    return blocksize, stepsize, numberofblocks

def AlgoVersion2(length):
    if length <= 512 * 1024 * 1024:
        return AlgoVersion2Sub(length)
    else:
        return AlgoVersion2Sub(length, 1000)

def TrivialPrettyPrintDER(data):
    while len(data) > 0:
        if data[0] == 0x30:
            data = data[1:]
            length = data[0]
            data = data[1:]
            if length > 128:
                newlength = 0
                for iter in range(length - 128):
                    newlength = newlength * 256 + data[0]
                    data = data[1:]
                length = newlength
            print('Sequence(%d)' % length)
        elif data[0] == 0x02:
            data = data[1:]
            length = data[0]
            data = data[1:]
            if length > 128:
                newlength = 0
                for iter in range(length - 128):
                    newlength = newlength * 256 + data[0]
                    data = data[1:]
                length = newlength
            integer = data[:length]
            data = data[length:]
            print('Integer(%d) %d' % (length, int.from_bytes(integer, 'big')))

METADATATYPE_UNKNOWN = 0
METADATATYPE_ALGO1 = 1
METADATATYPE_MULTIPLE_MAGICS = 2
METADATATYPE_FULL = 3
METADATATYPE_ALGO2 = 4
METADATATYPE_FULL_ALGO2 = 5

MAGIC_PARTIAL_ENCRYPTION = b'RANSOMWARE_METADATA#'
MAGIC_FULL_ENCRYPTION_ALGO1 = b'RANSOMWARE_METADATA'
MAGIC_FULL_ENCRYPTION_ALGO2 = MAGIC_FULL_ENCRYPTION_ALGO1 + b'#'

def AddPadding(data, length=16):
    padding = length - len(data) % length
    return data + bytes([padding]) * padding
    
def AnalyzeMetadata(metadata):
    items = metadata.split(b'#')
    print('Magic:                  %s' % items[0].decode('latin'))
    testb64 = items[1]
    print('TESTB64:                %s' % testb64.decode('latin'))
    testb64 = binascii.a2b_base64(testb64)
#    testb64_16 = AddPadding(b"TESTB64@''~") # sample 22af4ef1efde7a604e0e019c6d2be02f2eec10c637d0a857d73f7cfc5e83752d.vir
    testb64_16 = AddPadding(b'TESTB64')
    testb64keystream = bytes([testb64[i] ^ testb64_16[i] for i in range(len(testb64_16))])
    print('Keystream[:16]:         %s' % binascii.b2a_hex(testb64keystream).decode('latin'))
    index = 2
    metadataType = METADATATYPE_ALGO1
    if b'$' in items[index]:
        metadataType = METADATATYPE_ALGO2
        print('Certificate:')
        for iter, item in enumerate(items[index].split(b'$')):
            hexdata = binascii.a2b_hex(item)
            if iter == 0:
                print('Item %d' % iter)
                print('Size %d' % len(hexdata))
                base64encoded = ''
                for line in hexdata.decode('latin').split('\n'):
                    line = line.rstrip('\n\r')
                    if line != '' and not '-' in line:
                        base64encoded += line
                TrivialPrettyPrintDER(binascii.a2b_base64(base64encoded))
            else:
                print('Item %d' % iter)
                print('Size %d' % len(hexdata))
                print('Entropy: %s' % CalculateByteStatisticsNT(data=hexdata).entropystr)
            print()
        index += 1
    return METADATATYPE_FULL_ALGO2, testb64keystream

def AnalyzeEncrypted(data):
    positions = FindAll(data, MAGIC_PARTIAL_ENCRYPTION)
    if len(positions) == 0:
        if data.endswith(MAGIC_FULL_ENCRYPTION_ALGO1):
            print('Magic:                  %s' % MAGIC_FULL_ENCRYPTION_ALGO1.decode('latin'))
            return [METADATATYPE_FULL]
        else:
            positions = FindAll(data, MAGIC_FULL_ENCRYPTION_ALGO2)
            if len(positions) == 0:
                return [METADATATYPE_UNKNOWN]
            elif len(positions) == 1:
                result = AnalyzeMetadata(data[positions[0]:])
                return result[0], data[:positions[0]], len(data[:positions[0]]), 0, 1, result[1], b''
            else:
                return METADATATYPE_MULTIPLE_MAGICS, positions
    elif len(positions) == 1:
        trailer = data[positions[0]:]
        items = trailer.split(b'#')
        print('Magic:                  %s' % items[0].decode('latin'))
        testb64 = items[1]
        print('TESTB64:                %s' % testb64.decode('latin'))
        testb64 = binascii.a2b_base64(testb64)
#        testb64_16 = AddPadding(b"TESTB64@''~") # sample 22af4ef1efde7a604e0e019c6d2be02f2eec10c637d0a857d73f7cfc5e83752d.vir
        testb64_16 = AddPadding(b'TESTB64')
        testb64keystream = bytes([testb64[i] ^ testb64_16[i] for i in range(len(testb64_16))])
        print('Keystream[:16]:         %s' % binascii.b2a_hex(testb64keystream).decode('latin'))
        index = 2
        metadataType = METADATATYPE_ALGO1
        if b'$' in items[index]:
            metadataType = METADATATYPE_ALGO2
            print('Certificate:')
            for iter, item in enumerate(items[index].split(b'$')):
                hexdata = binascii.a2b_hex(item)
                if iter == 0:
                    print('Item %d' % iter)
                    print('Size %d' % len(hexdata))
                    base64encoded = ''
                    for line in hexdata.decode('latin').split('\n'):
                        line = line.rstrip('\n\r')
                        if line != '' and not '-' in line:
                            base64encoded += line
                    TrivialPrettyPrintDER(binascii.a2b_base64(base64encoded))
                else:
                    print('Item %d' % iter)
                    print('Size %d' % len(hexdata))
                    print('Entropy: %s' % CalculateByteStatisticsNT(data=hexdata).entropystr)
                print()
            index += 1
        ranges = items[index:]
        start, blocksize = [int(x) for x in ranges[0].decode('latin').split(':')]
        stepsize, blocksize_ = [int(x) for x in ranges[1].decode('latin').split(':')]
        stepsize = stepsize - start
        if start != 0:
            print('Start is not 0: %d' % start)
        headerDecrypted = bytes([data[i + start] ^ testb64keystream[i] for i in range(len(testb64_16))])
        print('Decrypted header:       %s' % binascii.b2a_hex(headerDecrypted).decode('latin'))
        print('Decrypted header ASCII: %s' % ExtraInfoHEADASCII(headerDecrypted))
        print('blocksize:       %10d' % blocksize)
        print('stepsize:        %10d' % stepsize)
        start = 0
        for range_ in ranges:
            range_ = range_.decode('latin')
            rangeExpected = '%d:%d' % (start, blocksize)
            start += stepsize
            if range_ != rangeExpected:
                print('Unexpected range: %s (expected %s)' % (range_, rangeExpected))
        numberofblocks = len(ranges)
        print('numberofblocks:  %10d' % numberofblocks)
        return metadataType, data[:positions[0]], blocksize, stepsize, numberofblocks, testb64keystream, headerDecrypted
    else:
        return METADATATYPE_MULTIPLE_MAGICS, positions

def ProcessBinaryFile(filename, content, cutexpression, flag, oOutput, oLogfile, options, oParserFlag):
    global fileCounter
    global fileStarttime

    lastWriteTime = FormatTime(os.path.getmtime(filename))
#    if not lastWriteTime.startswith('20230823'):
#        oLogfile.Line('info', 'wrongdate', filename, lastWriteTime)
#        return

    if content == None:
        try:
            oBinaryFile = cBinaryFile(filename, C2BIP3(options.password), options.noextraction, options.literalfilenames)
        except:
            oLogfile.LineError('Opening file %s %s' % (filename, repr(sys.exc_info()[1])))
            return
        oLogfile.Line('Success', 'Opening file %s' % filename)
        try:
            data = oBinaryFile.read()
        except:
            oLogfile.LineError('Reading file %s %s' % (filename, repr(sys.exc_info()[1])))
            return
        data = CutData(data, cutexpression)[0]
        oBinaryFile.close()
    else:
        data = content

    (flagoptions, flagargs) = oParserFlag.parse_args(flag.split(' '))

    fileCounter += 1

    try:
        dataHEXHEAD = binascii.b2a_hex(data[:8])
        dataHEXASCII = ExtraInfoHEADASCII(data)
        oOutput.Line('%s Processing file: %d %d %s (%s %s %s)' % (FormatTime(), fileCounter, time.time() - fileStarttime, filename, lastWriteTime, dataHEXHEAD, dataHEXASCII))
        oLogfile.Line('info', 'processfile', filename, lastWriteTime, dataHEXHEAD, dataHEXASCII, len(data), hashlib.sha256(data).hexdigest(), hashlib.md5(data).hexdigest())

        result = AnalyzeEncrypted(data)
        if result[0] == METADATATYPE_UNKNOWN:
            oOutput.Line('No encryption trailer found')
        elif result[0] == METADATATYPE_ALGO1:
            oOutput.Line('Encryption trailer algo1 found')
            data = result[1]
        elif result[0] == METADATATYPE_ALGO2:
            oOutput.Line('Encryption trailer algo2 found')
            data = result[1]
        else:
            oOutput.Line('Multiple encryption trailers found')
            return

        result1b = AlgoVersion2(len(data))
        print()
        print('Calculation encrypted:')
        print(' blocksize:      %10d' % result1b[0])
        print(' stepsize:       %10d' % result1b[1])
        print(' numberofblocks: %10d' % result1b[2])
        if result[0] == 1 and result[2:] != result1b:
            raise Exception('Difference!')

        baData = bytearray(data)
        if options.force1:
            if len(baData) <= 512 * 1024 * 1024:
                blocksize, stepsize, numberofblocks = AlgoVersion1(len(baData))
            else:
                blocksize, stepsize, numberofblocks = AlgoVersion1(len(baData), 1000)
        else:
            blocksize, stepsize, numberofblocks = AlgoVersion2(len(baData))

        if result[0] == METADATATYPE_ALGO2:
            dummy, data, blocksize, stepsize, numberofblocks, testb64keystream, headerDecrypted = result
            for step in range(numberofblocks):
                for i in range(blocksize):
                    baData[step * stepsize + i] ^= DECRYPTIONSTREAM[i % 16]
        else:
            if blocksize > len(DECRYPTIONSTREAM):
                oOutput.Line('Warning: file too large, skipping: %s %d' % (filename, len(data)))
                oLogfile.Line('warning', 'filetoolarge', filename, len(data), hashlib.sha256(data).hexdigest(), hashlib.md5(data).hexdigest())
                return
            for step in range(numberofblocks):
                for i in range(blocksize):
                    baData[step * stepsize + i] ^= DECRYPTIONSTREAM[i]

        baDataSHA256 = hashlib.sha256(baData).hexdigest()
        baDataMD5 = hashlib.md5(baData).hexdigest()
        baDataHEXHEAD = binascii.b2a_hex(baData[:8])
        baDataHEXASCII = ExtraInfoHEADASCII(baData)
#        if not baData[:6] in [b'AC1002', b'AC1003', b'AC1004', b'AC1006', b'AC1009', b'AC1012', b'AC1014', b'AC1015', b'AC1018', b'AC1021', b'AC1024', b'AC1027', b'AC1032']:
#            oLogfile.Line('info', 'decryptrionunexpectedheader', filename, baDataHEXHEAD, baDataHEXASCII, len(baData), baDataSHA256, baDataMD5)
#            oOutput.Line('  Skip: %s %s' % (baDataHEXHEAD, baDataHEXASCII))
#            return
        oLogfile.Line('info', 'startwritefile', filename, baDataHEXHEAD, baDataHEXASCII, len(baData), numberofblocks, baDataSHA256, baDataMD5)
        if filename.lower().endswith('.encrypted'):
            filename = filename[:-10]
        else:
            filename += '.Decrypted'
        with open(filename, 'wb') as fOut:
            fOut.write(baData)
        oLogfile.Line('info', 'endwritefile', filename, baDataHEXHEAD, baDataHEXASCII, len(baData), numberofblocks, baDataSHA256, baDataMD5)
        oOutput.Line('  Done: %s %s' % (baDataHEXHEAD, baDataHEXASCII))
    except:
        oLogfile.LineError('Processing file %s %s' % (filename, repr(sys.exc_info()[1])))
        if not options.ignoreprocessingerrors:
            raise

#    data = CutData(cBinaryFile(filename, C2BIP3(options.password), options.noextraction, options.literalfilenames).Data(), cutexpression)[0]

def RemoveFilesFromPriorRuns(filenames, filenamedatabase):
    jsonfilename = 'filenamedatabase-%s.json' % filenamedatabase
    if not os.path.exists(jsonfilename):
        return filenames, {}

    dDatabase = json.load(open(jsonfilename, 'r'))
    return [filename for filename in filenames if filename[0] not in dDatabase.keys()], dDatabase

def AddFilesToPriorRunsDatabase(dDatabase, filenamedatabase):
    jsonfilename = 'filenamedatabase-%s.json' % filenamedatabase
    json.dump(dDatabase, open(jsonfilename, 'w'))

def ProcessBinaryFiles(filenames, oLogfile, options, oParserFlag):
    global DECRYPTIONSTREAM

    if options.keystream != '':
        with open(options.keystream, 'rb') as fIn:
            DECRYPTIONSTREAM = fIn.read()

    oOutput = InstantiateCOutput(options)
    index = 0
    if options.jsoninput:
        items = CheckJSON(sys.stdin.read())
        if items == None:
            return
        for item in items:
            oOutput.Filename(item['name'], index, len(items))
            index += 1
            ProcessBinaryFile(item['name'], item['content'], '', '', oOutput, oLogfile, options, oParserFlag)
    else:
        if options.filenamedatabase != '':
            filenames, dDatabaseFilenames = RemoveFilesFromPriorRuns(filenames, options.filenamedatabase)
        else:
            dDatabaseFilenames = {}

        for filename, cutexpression, flag in filenames:
            oOutput.Filename(filename, index, len(filenames))
            index += 1
            dDatabaseFilenames[filename] = time.time()
            ProcessBinaryFile(filename, None, cutexpression, flag, oOutput, oLogfile, options, oParserFlag)

        if options.filenamedatabase != '':
            AddFilesToPriorRunsDatabase(dDatabaseFilenames, options.filenamedatabase)

def Main():
    moredesc = '''

Copyright NVISO 2023
Use at your own risk'''

    oParserFlag = optparse.OptionParser(usage='\nFlag arguments start with #f#:')
    oParserFlag.add_option('-l', '--length', action='store_true', default=False, help='Print length of files')

    oParser = optparse.OptionParser(usage='usage: %prog [options] [[@]file|cut-expression|flag-expression ...]\n' + __description__ + moredesc, version='%prog ' + __version__, epilog='This tool also accepts flag arguments (#f#), read the man page (-m) for more info.')
    oParser.add_option('-m', '--man', action='store_true', default=False, help='Print manual')
    oParser.add_option('-k', '--keystream', type=str, default='', help='File containing keystream')
    oParser.add_option('-o', '--output', type=str, default='', help='Output to file (# supported)')
    oParser.add_option('-p', '--password', default='infected', help='The ZIP password to be used (default infected)')
    oParser.add_option('-n', '--noextraction', action='store_true', default=True, help='Do not extract from archive file')
    oParser.add_option('-l', '--literalfilenames', action='store_true', default=False, help='Do not interpret filenames')
    oParser.add_option('-r', '--recursedir', action='store_true', default=False, help='Recurse directories (wildcards and here files (@...) allowed)')
    oParser.add_option('--force1', action='store_true', default=False, help='Force algo 1')
    oParser.add_option('--checkfilenames', action='store_true', default=False, help='Perform check if files exist prior to file processing')
    oParser.add_option('-j', '--jsoninput', action='store_true', default=False, help='Consume JSON from stdin')
    oParser.add_option('--logfile', type=str, default='', help='Create logfile with given keyword')
    oParser.add_option('--logcomment', type=str, default='', help='A string with comments to be included in the log file')
    oParser.add_option('--ignoreprocessingerrors', action='store_true', default=False, help='Ignore errors during file processing')
    oParser.add_option('--filenamedatabase', type=str, default='', help='Use this to skip files that have bene processed in prior runs')

#    oParser.add_option('-s', '--select', default='', help='select item nr for dumping')
#    oParser.add_option('-d', '--dump', action='store_true', default=False, help='perform dump')
#    oParser.add_option('-x', '--hexdump', action='store_true', default=False, help='perform hex dump')
#    oParser.add_option('-X', '--hexdumpnows', action='store_true', default=False, help='perform hex dump without whitespace')
#    oParser.add_option('-a', '--asciidump', action='store_true', default=False, help='perform ascii dump')
#    oParser.add_option('-A', '--asciidumprle', action='store_true', default=False, help='perform ascii dump with RLE')
#    oParser.add_option('-b', '--base64', action='store_true', default=False, help='perform BASE64 dump')
#    oParser.add_option('-B', '--base64nows', action='store_true', default=False, help='perform BASE64 dump without whitespace')

    (options, args) = oParser.parse_args()

    if options.man:
        oParser.print_help()
        oParserFlag.print_help()
        PrintManual()
        return

    if len(args) != 0 and options.jsoninput:
        print('Error: option -j can not be used with files')
        return

    oLogfile = cLogfile(options.logfile, options.logcomment)
    oExpandFilenameArguments = cExpandFilenameArguments(args, options.literalfilenames, options.recursedir, options.checkfilenames, '#c#', '#f#')
    oLogfile.Line('FilesCount', str(len(oExpandFilenameArguments.Filenames())))
#    oLogfile.Line('Files', repr(oExpandFilenameArguments.Filenames()))
    if oExpandFilenameArguments.warning:
        PrintError('\nWarning:')
        PrintError(oExpandFilenameArguments.message)
        oLogfile.Line('Warning', repr(oExpandFilenameArguments.message))

    ProcessBinaryFiles(oExpandFilenameArguments.Filenames(), oLogfile, options, oParserFlag)

    if oLogfile.errors > 0:
        PrintError('Number of errors: %d' % oLogfile.errors)
    oLogfile.Close()

if __name__ == '__main__':
    Main()
