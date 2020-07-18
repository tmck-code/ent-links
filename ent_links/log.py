'''
A very thin wrapper around python logging, which removes boilerplate in many files
'''

import logging

logging.basicConfig(format='%(asctime)s - %(name)-20s - %(levelname)-s - %(message)s')

# This getLogger name matches the standard lib one! But this violates linter naming conventions
# pylint: disable=invalid-name
def getLogger(name):
    'Returns a logger that will actually print output when set to INFO level'
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
