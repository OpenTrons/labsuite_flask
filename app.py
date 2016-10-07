from flask import Flask, request
import json
import hashlib
import os
from labsuite.compilers import pfusx
from OpenSSL import SSL

app = Flask(__name__)

context = ('certificate.crt', 'private.key')

@app.route('/compile/pfusx', methods=['GET', 'POST'])
def compile(text=None):
    """
    Send provided code to the designated compiler and outputs a JSON
    object detailing success or failure.

    Success looks like:

        {
            "success": true,
            "compiled_url": "http://example.com/rendered/foo.json",
            "return_data": {"description":"A1: atcgtactgatc"} 
        }

    Failure looks like:

        {
            "success": false,
            "errors": ["First input should be different."]
        }

    Errors can be output to the user and vary by compiler. They're often
    related to specific Mix.Bio form fields.
    """
    text = request.args.get('input').strip().split('\n')

    if not text:
        return "handle_response("+json.dumps({
            'success': False,
            'errors': ["No input provided."]
        })+")"

    # Compile the protocol, return any errors.
    try:
        protocol = pfusx.compile(*text)
    except Exception as e:
        return "handle_response("+json.dumps({'success': False, 'errors': [str(e)]})+")"

    description = json.loads(protocol)["info"]["description"]

    # Save the data as a hash in the public dir where it can be downloaded.
    content_hash = hashlib.sha224(protocol.encode('utf-8')).hexdigest()
    fpath = os.path.dirname(os.path.realpath(__file__))+"/static/protocols/"
    fname = "ot_one_"+content_hash+".json"

    with open(fpath+fname, 'w') as f:
        f.write(protocol)

    output = {
        "success": True,
        "filename": 'https://api.mix.bio/static/protocols/'+fname,
        "return_data": {"description": description} 
    }

    return "handle_response("+json.dumps(output)+")"


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0', ssl_context=context, threaded=True) 
