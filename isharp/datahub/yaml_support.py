from isharp.arctic_broker.broker_impl.arctic_data_broker import  ArcticBroker
from isharp.csv_files.simple_file_broker import SimpleFileBroker
from arctic import Arctic
import yaml
import expandvars


def file_broker_constructor(loader,node):
    root_directory = expandvars.expandvars(node.value[0][1].value)
    print("setting up simple file broker against root dir {}".format(root_directory))
    return SimpleFileBroker(root_directory)

def mongo_broker_constructor (loader,node):
    mongo_location = expandvars.expandvars(node.value[0][1].value)
    print("setting up arctic broker against host {}".format(mongo_location))
    arctic = Arctic(mongo_location)
    return ArcticBroker(arctic)


def set_up_unsafe_loader():
    yaml.add_constructor("!SimpleFileBroker", file_broker_constructor,yaml.UnsafeLoader)
    yaml.add_constructor("!ArcticBroker", mongo_broker_constructor,yaml.UnsafeLoader)








