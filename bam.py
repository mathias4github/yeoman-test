# BGP Atlas Monitor

import argparse, os, json
from flask import Flask
from flask.ext.cache import Cache



# Our own modules
import lib.www.pages
from lib.tools.get_announced_prefixes import *
from lib.tools.get_visibility import *
from lib.tools.get_visibility_prefix import *
from lib.tools.get_probes import *


# The Flask application
app = Flask(__name__,
            template_folder="data/www/templates/",
            static_folder="data/www/static/",
            static_url_path="/static")
cache = Cache(app,config={'CACHE_TYPE': 'simple'})


@app.route("/")
def flask_index():
  """BAM index"""

  return lib.www.pages.index(app.config["CONFIG"])


@app.route("/get_prefixes")
@app.route("/get_prefixes/<int:asn>")
@cache.cached()
def flask_get_prefixes(asn=None):
  """Return the list of prefixes as seen by RIPE stat"""

  if asn == None:
    asn = app.config["CONFIG"]["asn"]

  doc = get_announced_prefixes(asn)
  doc["asn"] = asn

  return json.dumps(doc)


@app.route("/get_visibility")
@app.route("/get_visibility/<int:asn>")
@cache.cached()
def flask_get_visibility(asn=None):
  """Return the visibility of an AS as seen by RIPE stat."""

  if asn == None:
    asn = app.config["CONFIG"]["asn"]

  visibilities = get_visibility(asn)

  doc = {}
  doc["asn"] = asn
  doc["visibilities"] = visibilities

  return json.dumps(doc)


@app.route("/get_visibility_prefix/<path:prefix>")
@cache.cached()
def flask_get_visibility_prefix(prefix):
  """Return the visibility of a prefix as seen by RIPE stat."""

  visibilities = get_visibility_prefix(prefix)

  doc = {}
  doc["prefix"] = prefix
  doc["visibilities"] = visibilities

  return json.dumps(doc)


@app.route("/get_probes")
@app.route("/get_probes/<int:asn>")
@cache.cached()
def flask_get_probes(asn=None):
  """Return the probes contained in an ASN."""

  if asn == None:
    asn = app.config["CONFIG"]["asn"]

  probes = get_probes(asn)

  doc = {}
  doc["asn"] = asn
  doc["probes"] = probes

  return json.dumps(probes)


if __name__ == '__main__':

  # Parse command line options
  parser = argparse.ArgumentParser("BGP Atlas Monitor")
  parser.add_argument("-t", "--timeout", dest="timeout", type=int, default=60, help="The cache timeout")
  parser.add_argument("-d", "--debug", dest="debug", action="store_true", default=False, help="Run in debug mode")
  parser.add_argument("asn", type=int, help="The AS number that will be monitored")
  args = parser.parse_args()

  # Global config
  config = {}
  config["asn"] = args.asn

  # Configure Flask
  app.config["CONFIG"] = config
  app.config["DEBUG"] = args.debug
  app.config["CSRF_ENABLED"] = True
  app.config["SECRET_KEY"] = os.urandom(128)
  app.config["CACHE_DEFAULT_TIMEOUT"] = args.timeout

  # Start Flask
  app.run()
