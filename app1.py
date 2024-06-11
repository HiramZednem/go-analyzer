import re
from flask import Flask, render_template, request

app = Flask(__name__)

# Conjuntos de palabras reservadas y símbolos para Go
reserved_words = {'package', 'import', 'func', 'main', 'fmt', 'Println'}
symbols = {';', '+', '=', ',', '{', '}', '(', ')', '.'}
identifiers = {'fmt'}

def analyze_code(code):
    lines = code.split('\n')
    tokens = []
    errors = []

    # Inicializar contadores
    counts = {
        'reserved_words': 0,
        'symbols': 0,
        'identifiers': 0,
        'numbers': 0,
        'left_paren': 0,
        'right_paren': 0,
        'left_brace': 0,
        'right_brace': 0,
        'lexical_errors': 0
    }

    for i, line in enumerate(lines, start=1):
        # Utilizar expresiones regulares para encontrar palabras y símbolos, incluyendo cadenas de texto
        words = re.findall(r'".*?"|\b\w+\b|[\(\){};"+=,.]', line)
        for word in words:
            token = {
                'token': word,
                'line': i,
                'reserved': 'x' if word in reserved_words else '',
                'symbol': 'x' if word in symbols else '',
                'left_paren': 'x' if word == '(' else '',
                'right_paren': 'x' if word == ')' else '',
                'left_brace': 'x' if word == '{' else '',
                'right_brace': 'x' if word == '}' else '',
                'number': 'x' if word.isdigit() else '',
                'identifier': 'x' if word in identifiers or re.match(r'".*?"', word) else '',
                'lexical_error': ''
            }

            # Verificar si hay errores léxicos
            if not any([word in reserved_words, word in symbols,
                        word == '(', word == ')', word == '{', word == '}',
                        word.isdigit(), word in identifiers, re.match(r'".*?"', word)]):
                token['lexical_error'] = 'x'
                counts['lexical_errors'] += 1
                errors.append({'line': i, 'error': f'Illegal character or token: {word}'})

            # Incrementar contadores
            if token['reserved']:
                counts['reserved_words'] += 1
            if token['symbol']:
                counts['symbols'] += 1
            if token['identifier']:
                counts['identifiers'] += 1
            if token['number']:
                counts['numbers'] += 1
            if token['left_paren']:
                counts['left_paren'] += 1
            if token['right_paren']:
                counts['right_paren'] += 1
            if token['left_brace']:
                counts['left_brace'] += 1
            if token['right_brace']:
                counts['right_brace'] += 1

            tokens.append(token)

    return tokens, counts, errors

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form['code']
        tokens, counts, errors = analyze_code(code)
        return render_template('index.html', tokens=tokens, code=code, counts=counts, errors=errors)
    return render_template('index.html', tokens=[], code='', counts={}, errors=[])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
