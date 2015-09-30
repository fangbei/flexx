"""
JavaScript minification tools.
"""

def minify(code, remove_whitespace=True):
    """ Main minification function.
    
    Removes comments. If remove_whitespace is True, removes all
    non-functional whitespace. Otherwise remove all trailing whitespace
    and indents using tabs to preserve space.
    """
    code = remove_singleline_comments(code)
    code = remove_multiline_comments(code)
    if remove_whitespace:
        code = remove_all_whitespace(code)
    else:
        code = remove_trailing_whitespace(code)
        code = tabbify(code)
    return code

def remove_singleline_comments(code):
    lines = []
    for line in code.splitlines():
        pre, _, post = line.partition('//')
        pre = pre.rstrip()
        if pre:
            lines.append(pre)
    return '\n'.join(lines)

def remove_multiline_comments(code):
    chars = ['\n']
    class non_local: pass
    non_local._i = -1
    
    def read():
        non_local._i += 1
        if non_local._i < len(code):
            return code[non_local._i]
    def to_end_of_string(c0):
        chars.append(c0)
        while True:
            c = read()
            chars.append(c)
            if c == c0 and chars[-1] != '\\':
                return
    def to_end_of_mutiline_comment():
        lastchar = ''
        while True:
            c = read()
            if c == '/' and lastchar == '*':
                return
            lastchar = c
    while True:
        c = read()
        if not c:
            break  # end of code
        elif c == "'" or c == '"':
            to_end_of_string(c)
        elif c == '*' and chars[-1] == '/':
            chars.pop(-1)
            to_end_of_mutiline_comment()
        else:
            chars.append(c)
    chars.pop(0)
    return ''.join(chars)

def remove_all_whitespace(code):
    code = code.replace('\t', ' ').replace('\r', ' ').replace('\n', ' ')
    space_safe = ' =+-/*&|(){},.><:;'
    chars = ['\n']
    class non_local: pass
    non_local._i = -1
    
    def read():
        non_local._i += 1
        if non_local._i < len(code):
            return code[non_local._i]
    while True:
        c = read()
        if not c:
            break  # end of code
        if c in ' ':
            if chars[-1] not in space_safe:
                chars.append(c)
        elif c in space_safe and chars[-1] == ' ':
            chars[-1] = c  # replace last char
        else:
            chars.append(c)
    chars.pop(0)
    return ''.join(chars)
    
def remove_trailing_whitespace(code):
    return '\n'.join([line.rstrip() for line in code.splitlines()])

def tabbify(code):
    lines = []
    for line in code.splitlines():
        line2 = line.lstrip()
        indent = (len(line)-len(line2)) // 4
        lines.append('\t'*indent + line2)
    return '\n'.join(lines)
    