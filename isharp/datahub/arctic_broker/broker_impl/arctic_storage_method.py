from isharp.datahub.core import *
from typing import List
import logging
import dataclasses
logging.basicConfig(level=logging.INFO)



def tokenize_path(path) -> List[str]:
    tokens = [i for i in list(path.split('/')) if len(i) > 0]
    return tokens




class TreeBuilder:
    def __init__(self,tickers,library_name,initial_path) -> None:
        super().__init__()
        self.tickers = tickers
        self.library_name = library_name
        self.initial_path = initial_path


    def build(self)->DirectoryNode:
        tokenized_initial_path = tokenize_path(self.initial_path)
        filtered_tickers = self.tickers
        child_list = []
        if tokenized_initial_path :
            target_path = '.'.join(tokenized_initial_path)
            filtered_tickers = filter(lambda thisTicker : target_path in thisTicker,self.tickers)

        strip_element_pos = len(tokenized_initial_path)
        for this_ticker in filtered_tickers:
            ticker_tokens = [i for i in list(this_ticker.split('.')) if len(i) > 0]
            if len(ticker_tokens) > strip_element_pos:
                child_list.append(ticker_tokens[strip_element_pos])

        sorted_deduped_children = list(set(child_list))
        sorted_deduped_children.sort()

        return  DirectoryNode(children=sorted_deduped_children,path = ([self.library_name] + tokenized_initial_path))



class ArcticStorageMethod(StorageMethod):

    def __init__(self,store):
        self.store = store
        super().__init__("arctic")

    def _lib_ticker(self,path):
        tokens = tokenize_path(path)
        library = tokens[0]
        ticker = '.'.join(tokens[1:])
        logging.info("Arctic storage method converted path to libaray [{}], ticker [{}]".format(library,ticker))

        if  library in self.store.list_libraries():
            lib = self.store[library]
            if lib.has_symbol(ticker):
                versioned  = lib.read(ticker)
                return (library,ticker)

            else:
                raise StorageMethod.ResourceException("ticker {} not found".format(ticker))
        else:
            raise StorageMethod.ResourceException("library {} not found in library list {}".format(library,self.store.list_libraries()))

        return (library, ticker)

    def acquireContent(self, path, params, version_id=None)->AcquireContentReturnValue:
        library, ticker = self._lib_ticker(path)
        lib = self.store[library]
        v = None if version_id is None else int(version_id)
        versioned  = lib.read(ticker, v)
        header = MatrixHeader(
        name= path,
        revision_id= str(versioned.version),
        storage_method=self.name,
        path= path,
        memory_style=MemStyles.DATA_FRAME,
        description=None
        )


        return AcquireContentReturnValue(content=versioned.data,header=header)




    def storeContent(self, path, params, content,revision_info)->Revision:

        library, ticker = self._lib_ticker(path)

        _store_content(self.store[library],ticker,content,revision_info)

    def history(self,matrix_url)->List[Revision]:
        library, ticker = self._lib_ticker(matrix_url.url_components.path)
        lib = self.store[library]
        meta = lib.read_metadata(ticker)
        logging.info("attempted to get history for : {},{} result = [{}]".format(library, ticker,meta))
        if meta.metadata is None:
            return []
        else:
            return get_revisions_from_metadata(meta.metadata)

    def dir(self,path)->DirectoryNode:
        logging.info("arctic getting diir for {}".format(path))
        tokens = tokenize_path(path)
        if tokens:
            library_name = tokens.pop(0)
            library = self.store[library_name]
            tickers = library.list_symbols()
            t= TreeBuilder(tickers,library_name,"/".join(tokens))
            ret_val:DirectoryNode = t.build()


            return ret_val

        else:
            logging.info("arctic getting root directory for {}".format(path))
            libs = self.store.list_libraries()
            logging.info("arctic  gpt libraries {}".format(len(libs)))
            ret_val = DirectoryNode(children=libs,path=[])
            logging.info("returning directory node {}".format(len(ret_val.children)))
            return ret_val

    def list(self) -> List[MatrixHeader]:
        ret_val = []
        for this_lib_name in self.store.list_libraries():
            library = self.store[this_lib_name]
            for this_symbol in library.list_symbols():
                versions = library.list_versions(this_symbol)
                filtered = [version for version in versions if not version['deleted']]
                max_version = max(map(lambda v: v['version'], filtered))
                symbol_with_slashes = this_symbol.replace('.','/')
                ret_val.append(MatrixHeader(name=symbol_with_slashes,
                                            description="don't know yet",
                                            storage_method = self.name,
                                            memory_style = MemStyles.DATA_FRAME,
                                            revision_id = str(max_version),
                                            path="{}/{}".format(this_lib_name,symbol_with_slashes)))

        return ret_val






history_tag = "revision_history"

def add_revision_to_metadata(revision:Revision,metadata:dict,dict_key:str=history_tag):
    if metadata.get(dict_key) is None:
        metadata[dict_key] = []
    metadata[dict_key].append(dataclasses.asdict(revision))

def _revision_from_dict(dict:dict)->Revision:
    #todo ... there must be a better whay of doing this !
    revision_id = dict['id']
    revision_info = dict["revision_info"]
    return Revision(revision_id,RevisionInfo(who=revision_info['who'],what=revision_info['what'],when=revision_info['when']))


def get_revisions_from_metadata(metadata:dict,dict_key:str=history_tag)->List[Revision]:
    revision_list = metadata[dict_key]
    logging.info("retrieved revision list from  metadata: {}".format(revision_list))
    if revision_list is not  None:
        return [_revision_from_dict(i) for i in revision_list]
    else:
        return []



def import_pandas(lib, pd, symbol_name,revision_info):
    meta = {}
    add_revision_to_metadata(Revision('1', revision_info), meta)
    lib.write(symbol_name, pd, meta)


def _store_content(lib,ticker,content,revision_info)->Revision:
        logging.info("storing content  {} {}".format(lib, ticker))
        original_meta_d = lib.read_metadata(ticker).metadata

        old_revisions = get_revisions_from_metadata(original_meta_d)
        last_revision = old_revisions[-1]
        next_revision_id = str(int(last_revision.id)+1)
        new_revision = Revision(next_revision_id,revision_info)
        add_revision_to_metadata(new_revision,original_meta_d)
        ret = lib.write(ticker,content,original_meta_d)
        return new_revision

