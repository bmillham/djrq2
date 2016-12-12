#encoding: utf-8

from xml.etree import ElementTree
from datetime import datetime
#import urllib
#import sys
import html


__author__="brian"

class MediaLibrary:
    """A class to read (not write) the xml created by winamp
       Tries to be as close to the nullsoftdb class as possible
    """

    def __init__(self, db='/home/brian/djrq2-workingcopy/djrq2/privatefilearea/RonD/sept 27 d.xml', verbose=False, html=False):
        print("Reading the winamp xml", db)

        self.xmlfile = db
        self.dbfields = {}
        self.fieldtypes = {}
        self.primaryindex = {}
        self.totalrecords = 0
        self.xmlformat = None
        self.encoding = None
        self.tree = None
        self.root = None
        self.html = html
        self.opendata()
        self.readheader()
        self.createfieldmap()
        self.readindex()

    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict['dfile']
        return odict

    def __setstate__(self, dict):
        self.__dict__.update(dict)
        self.opendata()

    def opendata(self):
        """Opens the data file"""
        self.tree = ElementTree.parse(self.xmlfile)

    def closedata(self):
        """Closes the data file"""
        self.dfile.close()

    def readheader(self):
        """Reads the header of the XML and figures out if it's a EZPLAYLIST or
           and Apple playlist export"""
        root = self.tree.getroot()
        self.root = root
        if root.tag == 'EZPLAYLIST':
            print('XML is EXPLAYLIST format')
            self.xmlformat = 'MEDIAFILE'
        elif root.tag == 'plist':
            print('XML is Apple format')
            self.xmlformat = 'plist'
        else:
            print('Unknown XML format: {}'.format(root))
            return

    def readindex(self):
        """Read the indexes from the xml"""
        self.primaryindex = [i for i, r in enumerate(self.fetchall())]
        self.totalrecords = len(self.primaryindex)
        print('Total records:', self.totalrecords)

    def fetchall(self):
        """Read all the records from the winamp xml"""
        fields = self.fieldmap
        intfields = ('filesize', 'trackno', 'length')
        for i, r in enumerate(self.root.findall(self.xmlformat)):
            row = {fields[k]:html.unescape(r.findtext(k).strip()) for k in fields}
            if row['artist'] == '' or row['album'] == '' or row['title'] == '':
                continue
            #for k in row:
            #    if row[k] == ' ': row[k] = ''
            for r in intfields:
                if row[r] == '':
                    row[r] = 0
                else:
                    row[r] = int(row[r])
                if r == 'filesize': row[r] = int(row[r] / 1000)
            #if r not in intfields:
            #    row[r] = html.unescape(row[r])
            row['lastmodified'] = 0
            row['bitrate'] = 0
            row['id'] = i
            yield row

    def __fetchoneez(self, idx):
        record = self.rowtemplate()
        offset = self.primaryindex[idx]
        if idx == self.totalrecords-1:
            self.dfile.seek(0,2)
            nextoffset = self.dfile.tell()
            self.dfile.seek(offset)
        else:
            nextoffset = self.primaryindex[idx+1]
        datalen = nextoffset - offset
        data = self.dfile.read(datalen)
        rec = BeautifulSoup(data.decode(self.encoding))
        for r in self.fieldmap:
            val = rec.find(r)
            if val is None:
                continue
            if r == 'bitrate':
                fval = 0
            elif (r == 'size'
                or r == 'track'
                or r == 'time'
                and val.string is not None):
                try:
                    fval = int(val.string)
                except:
                    fval = 0
            else:
                if val.string is None:
                    fval = None
                else:
                    fval = self.unescape(val.string).encode('utf-8')
            if r == 'size': fval /= 1000
            record[self.fieldmap[r]] = fval
        record['id'] = idx
        return record

    def __fetchoneapple(self, idx):
      record = self.rowtemplate()
      for l in self.dfile:
            lbs = BeautifulSoup(l.decode(self.encoding))
            key = lbs.find('key')
            if key is not None:
                k = key.string
                if k == "Track ID":
                    ival = lbs.find('integer')
                    if ival is not None:
                        if int(ival.string) != idx:
                            break

                if k in self.fieldmap:
                    ival = lbs.find('integer')
                    sval = lbs.find('string')
                    dval = lbs.find('date')
                    if ival is not None:
                        val = int(ival.string)
                        if k == 'Total Time': val /= 1000
                        record[self.fieldmap[k]] = val
                    elif sval is not None:
                        val = unicode(self.unescape(sval.string)).encode('utf-8')
                        if k == 'Location':
                            val = urllib.unquote(val.lstrip("file://localhost/"))
                        record[self.fieldmap[k]] = val
                    elif dval is not None:
                        record[self.fieldmap[k]] = self.utcdate(dval.string)
      record['id'] = idx
      return record

    def createfieldmap(self):
        """Map of xml to winamp fields"""
        if self.xmlformat == 'apple':
          self.fieldmap = { # Map of xml -> winamp fields
            'Track ID': 'id',
            'Name': 'title',
            'Artist': 'artist',
            'Album': 'album',
            'Year': 'year',
            'Track Number': 'trackno',
            'Total Time': 'length',
            'Date Added': 'lastmodified',
            'Size': 'filesize',
            'Bitrate': 'bitrate',
            'Location': 'filename',
          }
        else:
            self.fieldmap = {
             'ARTIST': 'artist',
             'TITLE': 'title',
             'YEAR': 'year',
             'ALBUM': 'album',
             'BITRATE': 'bitrate',
             'TIME': 'length',
             'SIZE': 'filesize',
             'FILENAME': 'filename',
             'TRACK': 'trackno',
             #'LASTMODIFIED': 'lastmodified',
            }
    def utcdate(self, d):
        """Changes the XML date to utc date"""
        d1 = d.replace('T', ' ')
        d1 = d1.replace('Z', '')
        try:
            date = datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ')
        except:
            date = None
        if not date:
          try:
            date = datetime.strptime(d, '%a %b %d %H:%M:%S %Y')
          except:
            date = None
        if not date:
            print("Failed to convert date: ", d)
        return date

    def rowtemplate(self):
        """Creates a blank row"""
        rowtemplate = {} # Create a blank row template, with all the keys
        for f in self.fieldmap.values():
            rowtemplate[f] = None

        return rowtemplate
