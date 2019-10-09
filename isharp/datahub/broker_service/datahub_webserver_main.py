#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import re
import sys
import isharp.datahub.yaml_support  as iYaml
import nameko.cli.main
import isharp.datahub.web.webconsole as web
from multiprocessing import Process

def main():
    web.app.run(host='0.0.0.0',port=80)

if __name__== "__main__" :
    main()


