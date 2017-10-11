from e3uhc import makefilepath, odict
from xlrd import open_workbook


def e3uhcpath(subdir=None, trailingsep=True):
    ''' Returns the parent path of the E3UHC module. If subdir is not None, include it in the path '''
    import os
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    if subdir is not None:
        tojoin = [path, subdir]
        if trailingsep: tojoin.append('') # This ensures it ends with a separator
        path = os.path.join(*tojoin) # e.g. ['/home/optima', 'tests', '']
    return path


class Databook(object):
    '''
    An object that duplicaets the functionality of an Excel sheet.
    '''
    
    def __init__(self, data=None):
        self.raw = data
        return None
    
    def __getitem__(self, key):
        '''
        Do things like
        databook[0,0]
        databook['Column name']
        etc.
        '''
        return item
    
    def __setitem__(self, key, val):
        ''' As above '''
        return None
    

# Define the default filename
default_filename = e3uhcpath('data')+'DCP3 V9_Table by Package for UHC Chapter_Working Version_8 30 17.xlsx' # Include the Optima folder
default_sheetname = 'Deduplicated w Conflicts'


def loaddcp(filename=None, folder=None, sheetname=default_sheetname):
    '''
    Load the DCP database.
    '''
    fullpath = makefilepath(filename=filename, folder=folder, default=default_filename)
    workbook = open_workbook(fullpath)
    sheet = workbook.sheet_by_name(sheetname)
    
#    dcp = Databook()

    rawdcp = []
    for rownum in range(sheet.nrows-1):
        rawdcp.append(odict())
        for colnum in range(sheet.ncols):
            attr = sheet.cell_value(0,colnum)
            rawdcp[rownum][attr] = sheet.cell_value(rownum+1,colnum) if sheet.cell_value(rownum+1,colnum)!='None' else None
    return rawdcp