from os.path import dirname, basename, isfile, join
import glob
from importlib import import_module

import uvicorn
from fastapi import FastAPI

from dao import create_all_containers
from middleware import check_headers

app = FastAPI()

app.middleware("http")(check_headers)

modules = glob.glob(join(dirname(__file__), "endpoints/*.py"))
for f in modules:
    if isfile(f) and not f.endswith('__init__.py'):
        module = import_module('endpoints.%s' % basename(f)[:-3])
        app.include_router(getattr(module, "router"))

if __name__ == "__main__":
    create_all_containers()
    uvicorn.run(app, host="0.0.0.0", port=80)
