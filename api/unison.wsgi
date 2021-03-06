#!/usr/bin/env python
"""WSGI handler for Unison's REST API.

Tiny wrapper around Flask to add the proper paths to PYTONPATH. The virtual
environment setup is already done by mod_wsgi (see Apache config).
"""

import os
import sys
import yaml

# Redirect output to apache logs.
sys.stdout = sys.stderr

def application(environ, start_response):
    """Handle a request.

    Expects the UNISON_ROOT environment variable to be properly set by Apache.
    """
    # Matplotlib configuration directory - somehow needed by sklearn.
    os.environ['MPLCONFIGDIR']='/tmp'
    sys.path.insert(0, '%s/api/unison' % environ['UNISON_ROOT'])
    from unison import app
    # Set up configuration options.
    # TODO better logging.
    config = yaml.load(open('%s/config.yaml' % environ['UNISON_ROOT']))
    app.debug = config['debug']
    # Start the flask app.
    return app(environ, start_response)
