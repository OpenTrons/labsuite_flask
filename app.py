from flask import Flask
import json
import hashlib
import os

import pfusx

app = Flask(__name__)

@app.route('/compile/pfusx', methods=['POST'])
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

    text = text or request.form.pop('input', '').strip().split('\n')

    if not text:
        return json.dumps({
            'success': False,
            'errors': ["No input provided."]
        })

    # Compile the protocol, return any errors.
    try:
        protocol = pfusx.compile(text)
    except Exception as e:
        return {'success': False, 'errors': [str(e)]}

    description = json.loads(protocol)["info"]["description"]

    # Save the data as a hash in the public dir where it can be downloaded.
    content_hash = hashlib.sha224(protocol.encode('utf-8')).hexdigest()
    fpath = os.path.dirname(os.path.realpath(__file__))+"/static/protocols/"
    fname = "ot_one_"+content_hash+".json"

    with open(fpath+fname, 'w') as f:
        f.write(protocol)

    output = {
        "success": True,
        "filename": fname,
        "return_data": {"description": description} 
    }

    return json.dumps(output)


if __name__ == '__main__':
    app.run(debug=False, port=8080, host='0.0.0.0')