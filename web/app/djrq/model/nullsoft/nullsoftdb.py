import codecs
import struct
import re
from datetime import datetime

__author__="brian"
__date__ ="$Feb 6, 2011 1:38:17 AM$"

class MediaLibrary:
    """A class to read (not write) the database used by winamp"""
    
    def __init__(self, db, verbose=False):
        print "Reading the winamp database"
        self.idx = db + "/main.idx"
        self.dat = db + "/main.dat"
        self.verbose = verbose
        self.dbfields = {}
        self.fieldtypes = {}
        self.primaryindex = {}
        self.readindex()
        self.opendata()
        self.readheader()
        
    def opendata(self):
        self.dfile = open(self.dat, 'rb')
        #self.dfileunicode = codecs.open(self.dat, encoding='latin-1', mode='rb')
    
    def closedata(self):
        self.dfile.close()
        #self.dfileunicode.close()
        
    def readindex(self):
        ifile = open(self.idx, 'rb')
        header = ifile.read(8)
        if header != "NDEINDEX":
            print "Invalid index file"
            return None
        self.totalrecords = self.readint(ifile)
        myst = self.readint(ifile)
        cc = 0
        while cc < self.totalrecords:
            offset = self.readint(ifile)
            if offset < 0:
                print "Invalid offset %d!"%(offset)
                break
            ix = self.readint(ifile)
            self.primaryindex[ix] = offset
            cc += 1
        ifile.close()
        self.totalrecords = len(self.primaryindex) - 2
        
    def readheader(self):
        #print "Reading headers"

        # Read the dat header

        dheader = self.dfile.read(8)
        if dheader != "NDETABLE":
            print "Invalid data file"
            return None
        # Read the column names
        if self.verbose: print "\nReading column information" 
        while 1:
            dbf = self.readcolumnheader()
            self.dbfields[dbf['cid']] = dbf
            self.fieldtypes[dbf['colname']] = dbf['ctype']
            if dbf['next'] == 0: break
        if self.verbose: print "There are %d columns".format(len(self.dbfields))

    def readcolumnheader(self):
        """Read the column header from the winamp database"""
        column = self.readfieldinfo()
        column['ctype'] = self.readbyte()
        column['unique'] = self.readbyte()
        column['colname'] = self.readstring(True)
        return column
    
    def readfieldinfo(self):
        """Read the field information from the winamp database"""
        column = {}
        column['cid'] = self.readbyte()
        column['ftype'] = self.readbyte()
        column['size'] = self.readint()
        column['next'] = self.readint()
        column['prev'] = self.readint()
        if self.verbose:
            print "Column info:"
            print column
        
        return column
    
    def readshort(self):
        """Read a 2 byte signed short from the winamp database"""
        field = self.dfile.read(2)
        return struct.unpack("h", field)[0]

    def readushort(self):
        """Read a 2 byte unsigned short from the winamp database"""
        field = self.dfile.read(2)
        return struct.unpack("H", field)[0]

    def readbyte(self):
        """Read a 1 byte field from the winamp database"""
        field = self.dfile.read(1)
        if field == '':
            return -1
        return struct.unpack("B", field)[0]

    def readstring(self, iscolumnname=False):
        """Read a string from the winamp database, either regular or unicode"""
        if iscolumnname: # If its a column name, the size is byte not short
            msz = self.readbyte()
            ucode = 0
        else:
            msz = self.readshort()
            ucode = self.readushort()
        if ucode == 0xFEFF: # Unicode
            #msz -= 2
            self.dfile.seek(-2, 1)
            s = self.dfile.read(msz)
            fmt = "%ss"%(msz)
            field = struct.unpack(fmt,s)[0]
            try:
                f1 = field.decode('utf-16').encode('utf-8')
                #f1 = unicode(field.decode('utf-16'), 'utf-8')
                #print f1
            except:
                print "Decode/Encode failed!"
                print field
            else:
                field = f1
        else:
            if not iscolumnname:
                self.dfile.seek(-2,1) # Not unicode, go back 2 bytes and read the complete string
            field = self.dfile.read(msz)
        return field

    def readint(self, f=None):
        """Read a 4 byte integer from the winamp database
           If F is supplied, reads from that file, otherwise
           the default is to read from the data file
        """
        if not f: f = self.dfile
        field = f.read(4)
        if field == '':
            return -1
        return struct.unpack("i", field)[0]
    
    def fetchall(self):
        """Read all the records from the winamp database"""
        for i in self.primaryindex:
            if i < 2: continue # Skip the 2 header records
            row = self.fetchone(i)
            yield row
    
    def fetchone(self, idx):
      """Reads a single record from the winamp database"""
      if idx not in self.primaryindex:
          print "\nIndex %d is not a primary index"%(idx)
          return None
      self.dfile.seek(self.primaryindex[idx])
      pos = self.dfile.tell()
      if pos != self.primaryindex[idx]:
        print "ERROR: Failed to seek to index %d - %d!"%(idx, self.primaryindex['idx'])
        return None
      record = self.rowtemplate()
      times = []
      while 1:
        fl = self.readfieldinfo()
        if fl['ftype'] > 12 or fl['ftype'] == 0: return None
        if fl['cid'] not in self.dbfields.keys():
            print "\nColid %d not a defined field for row: %d" % (fl['cid'], idx)
            continue
        if fl['ftype'] == 4 or fl['ftype'] == 11: # Int and Length types
            ir = self.readint()
        elif fl['ftype'] == 10: # Date/Time type
            t = self.readint()
            ir = datetime.fromtimestamp(t)
            if self.dbfields[fl['cid']]['colname'] != 'lastplay': times.append(t)
        elif fl['ftype'] == 3 or fl['ftype'] == 12: # Strings types
            ir = self.readstring()
        else:
            print "Unknown type: %d" % fl['ftype']
            ir = "?"
        if fl['next'] == 0: break
        try:
            self.dfile.seek(fl['next'])
        except:
            print "Seek Failed!: %d" % fl['next']
            return None
        # Look at both date fields, and set the date to that
        if len(times) > 0:
            record['lastmodified'] = datetime.fromtimestamp(max(times))
        else:
            record['lastmodified'] = None
        record[self.dbfields[fl['cid']]['colname']] = ir

      record['id'] = idx
      return record

    def rowtemplate(self):
        rowtemplate = {} # Create a blank row template, with all the keys
        for f in self.dbfields:
            rowtemplate[self.dbfields[f]['colname']] = None
        return rowtemplate
    
