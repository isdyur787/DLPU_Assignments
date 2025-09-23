词法分析结果
==================================================
源文件: test_program.c
分析时间: 2025-09-21 11:07:10
==================================================

二元组 (单词种别码, 单词属性值):
==================================================
(  5, 'int       ') - INT
( 11, 'main      ') - MAIN
( 38, '(         ') - LEFT_PAREN
( 39, ')         ') - RIGHT_PAREN
( 31, '{         ') - LEFT_BRACE
(  5, 'int       ') - INT
( 46, 'a         ') - IDENTIFIER
( 25, '=         ') - ASSIGN
( 47,         10) - INTEGER
( 35, ';         ') - SEMICOLON
(  6, 'float     ') - FLOAT
( 46, 'b         ') - IDENTIFIER
( 25, '=         ') - ASSIGN
( 48,       3.14) - FLOAT_CONST
( 35, ';         ') - SEMICOLON
(  7, 'char      ') - CHAR
( 46, 'c         ') - IDENTIFIER
( 25, '=         ') - ASSIGN
( 50, ''A'       ') - CHAR_CONST
( 35, ';         ') - SEMICOLON
(  8, 'string    ') - STRING
( 46, 'message   ') - IDENTIFIER
( 25, '=         ') - ASSIGN
( 49, '"Hello World"') - STRING_CONST
( 35, ';         ') - SEMICOLON
(  1, 'if        ') - IF
( 38, '(         ') - LEFT_PAREN
( 46, 'a         ') - IDENTIFIER
( 29, '>         ') - GREATER
( 47,          5) - INTEGER
( 39, ')         ') - RIGHT_PAREN
( 31, '{         ') - LEFT_BRACE
( 12, 'printf    ') - PRINTF
( 38, '(         ') - LEFT_PAREN
( 49, '"a is greater than 5"') - STRING_CONST
( 39, ')         ') - RIGHT_PAREN
( 35, ';         ') - SEMICOLON
( 46, 'a         ') - IDENTIFIER
( 25, '=         ') - ASSIGN
( 46, 'a         ') - IDENTIFIER
( 21, '+         ') - PLUS
( 47,          1) - INTEGER
( 35, ';         ') - SEMICOLON
( 32, '}         ') - RIGHT_BRACE
(  2, 'else      ') - ELSE
( 31, '{         ') - LEFT_BRACE
( 46, 'a         ') - IDENTIFIER
( 25, '=         ') - ASSIGN
( 46, 'a         ') - IDENTIFIER
( 22, '-         ') - MINUS
( 47,          1) - INTEGER
( 35, ';         ') - SEMICOLON
( 32, '}         ') - RIGHT_BRACE
(  3, 'while     ') - WHILE
( 38, '(         ') - LEFT_PAREN
( 46, 'a         ') - IDENTIFIER
( 28, '<         ') - LESS
( 47,         20) - INTEGER
( 39, ')         ') - RIGHT_PAREN
( 31, '{         ') - LEFT_BRACE
( 46, 'a         ') - IDENTIFIER
( 25, '=         ') - ASSIGN
( 46, 'a         ') - IDENTIFIER
( 23, '*         ') - MULTIPLY
( 47,          2) - INTEGER
( 35, ';         ') - SEMICOLON
(  1, 'if        ') - IF
( 38, '(         ') - LEFT_PAREN
( 46, 'a         ') - IDENTIFIER
( 26, '==        ') - EQUAL
( 47,         16) - INTEGER
( 39, ')         ') - RIGHT_PAREN
( 14, 'break     ') - BREAK
( 35, ';         ') - SEMICOLON
( 32, '}         ') - RIGHT_BRACE
(  9, 'return    ') - RETURN
( 47,          0) - INTEGER
( 35, ';         ') - SEMICOLON
( 32, '}         ') - RIGHT_BRACE
==================================================
总共识别出 79 个单词符号
==================================================
分析完成