#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import re
import sys
import isharp.yaml_support  as iYaml
import nameko.cli.main
def main():
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    iYaml.set_up_unsafe_loader()
    sys.exit(nameko.cli.main.main())
