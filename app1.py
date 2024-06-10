import re
from flask import Flask, render_template, request

app = Flask(__name__)

# Conjuntos de palabras reservadas y símbolos para Go
reserved_words = {'package', 'import', 'func', 'main', 'fmt1','.','Println'}
symbols = {';', '"', '+', '=', ',', '{', '}', '(', ')', '.'}
identifiers = {'fmt','Hola','mundo'}

def analyze_code(code):
    lines = code.split('\n')
    tokens = []

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
        'lexical_errors': 0  # Agregar contador para errores léxicos
    }

    for i, line in enumerate(lines, start=1):
        # Utilizar expresiones regulares para encontrar palabras y símbolos
        words = re.findall(r'\b\w+\b|[\(\){};"+=,.]', line)
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
                'identifier': 'x' if word in identifiers else '',
                'lexical_error': 'x' if not any([word in reserved_words, word in symbols,
                                                  word == '(', word == ')', word == '{', word == '}',
                                                  word.isdigit(), word in identifiers]) else ''
                # Marcar como error léxico si ninguna categoría válida se identifica
            }

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

            # Contar errores léxicos
            if token['lexical_error']:
                counts['lexical_errors'] += 1

            tokens.append(token)

    return tokens, counts

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form['code']
        tokens, counts = analyze_code(code)
        return render_template('index.html', tokens=tokens, code=code, counts=counts)
    return render_template('index.html', tokens=[], code='', counts={})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
