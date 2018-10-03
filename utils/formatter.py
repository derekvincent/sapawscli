# -*- coding: utf-8 -*-

"""Output Formatter
Handles the output in different formats (json and tables)
"""

import json


def json_output(value):

    return json.dumps(
        value,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    )
