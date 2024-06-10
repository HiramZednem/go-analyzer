from flask import Flask, render_template, request
import lex
import yacc

app = Flask(__name__)

def analyze_code(code):
    lexer = lex.lexer
    parser = yacc.parser

    lexer.input(code)

    tokens = []
    token_counts = {}  # Diccionario para contar los tokens
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append({
            'token': tok.type,
            'value': tok.value,
            'line': tok.lineno,
            'position': tok.lexpos
        })
        token_counts[tok.type] = token_counts.get(tok.type, 0) + 1  # Contar el token

    # Parse the code
    parse_result = parser.parse(code)

    return tokens, parse_result, token_counts

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form['code']
        tokens, parse_result, token_counts = analyze_code(code)
        return render_template('index.html', tokens=tokens, code=code, parse_result=parse_result, counts=token_counts)
    return render_template('index.html', tokens=[], code='', parse_result=None, counts={})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
