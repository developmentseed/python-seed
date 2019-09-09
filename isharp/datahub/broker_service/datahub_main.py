#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import re
import sys
import isharp.datahub.yaml_support  as iYaml
import nameko.cli.main
import isharp.datahub.web.webconsole as web
from multiprocessing import Process
def runWeb():
    web.app.run(port=80)

def main():
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    iYaml.set_up_unsafe_loader()
    p = Process(target=runWeb)
    p.start()

    sys.exit(nameko.cli.main.main())

if __name__== "__main__" :
    main()


