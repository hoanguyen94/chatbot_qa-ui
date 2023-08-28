def splitChunk(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def checkColumns(realColumns: list, expectedColumns: list):
    # check for unexpected columns
    if not set(realColumns).issubset(expectedColumns):
        raise Exception(
            f'Wrong columns. Should only include columns {expectedColumns}')

    # check duplicate columns
    if len(set(realColumns)) != len(realColumns):
        raise Exception('There should not be columns')
    return
