import pandas as pd
def header_cols(header):
    return (header.name,
            header.storage_method,
            header.path,
            str(header.memory_style),
            header.description)

def mtx_headers_as_dataframe(matrix_headers):
    record_data = [header_cols(i) for i in matrix_headers]
    return pd.DataFrame.from_records(data= record_data, columns= ["name", "storage method", "path", "mem style", "description"])
