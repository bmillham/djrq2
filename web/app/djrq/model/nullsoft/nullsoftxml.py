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

    def __init__(self, db='/home/brian/djrq2-workingcopy/djrq2/privatefilearea/GothAlice/Library.xml', verbose=False, html=False):
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
        if self.xmlformat == 'MEDIAFILE':
            self.primaryindex = [r['id'] for r in self.__fetchallez()]
            self.totalrecords = len(self.primaryindex)
        elif self.xmlformat == 'plist':
            self._readplistindex()
        print('Total records:', self.totalrecords)

    def _readplistindex(self):
        """Read indexes for the apple formatted xml"""
        self.maindict = self.root.find('dict')
        # Find the tracks dict
        dictcount = 0
        dictloc = 0
        for k in self.maindict.findall('key'):
            if k.text in ('Tracks', 'Playlists'):
                if k.text == 'Tracks':
                    dictloc = dictcount # This is the dict with tracks
                dictcount += 1
        self.tracksdict = self.maindict.findall('dict')[dictloc]
        keys = self.tracksdict.findall('key')
        #self.primaryindex = [int(k.text) for k in keys]
        self.primaryindex = [r['id'] for r in self.__fetchallplist()]
        self.totalrecords = len(self.primaryindex)

    def fetchall(self):
        """Read all the records from the xml"""
        if self.xmlformat == 'MEDIAFILE':
            for r in self.__fetchallez():
                yield r
        elif self.xmlformat == 'plist':
            for r in self.__fetchallplist():
                yield r


    def __fetchallez(self):
        fields = self.fieldmap
        intfields = ('filesize', 'trackno', 'length')
        for i, r in enumerate(self.root.findall(self.xmlformat)):
            row = {fields[k]:html.unescape(r.findtext(k).strip()) for k in fields}
            unk_fields = ('artist', 'album', 'title')
            for f in unk_fields:
                if row[f] == '': row[f] = None
            for r in intfields:
                if row[r] == '':
                    row[r] = 0
                else:
                    row[r] = int(row[r])
                if r == 'filesize': row[r] = int(row[r] / 1000)
            row['lastmodified'] = 0
            row['bitrate'] = 0
            row['id'] = i
            yield row

    def __fetchallplist(self):
        fields = self.fieldmap
        pmap = {'Track ID': 'integer',
               'Name': 'string',
               'Artist': 'string',
               'Album': 'string',
               'Size': 'integer',
               'Total Time': 'integer',
               'Disc Number': 'integer',
               'Track Number': 'integer',
               'Year': 'integer',
               'Date Modified': 'date',
               'Date Added': 'date',
               'Bit Rate': 'integer',
               'Location': 'string',
               'Kind': 'string',
               'Track Type': 'string',
               'Persistent ID': 'string',
              }

        for trackdict in self.tracksdict.findall('dict'):
            tinfo = {}
            item = None
            for x in trackdict.iter():
                if x.tag == 'key':
                    item = x.text
                else:
                    if item in pmap:
                        if pmap[item] != x.tag:
                            print('ERROR:', pmap[item], x.tag)
                        tinfo[item] = x.text
                        if pmap[item] == 'integer':
                            tinfo[item] = int(tinfo[item])
                        elif pmap[item] == 'date':
                            try:
                                tinfo[item] = datetime.strptime(tinfo[item], "%Y-%m-%dT%H:%M:%S.%fZ")
                            except ValueError:
                                tinfo[item] = datetime.strptime(tinfo[item], "%Y-%m-%dT%H:%M:%SZ")
                        elif pmap[item] == 'string':
                            tinfo[item] = html.unescape(tinfo[item])

            if 'Kind' not in tinfo:
                #print('Missing kind', tinfo)
                continue
            if 'audio' in tinfo['Kind'].lower():
                if 'Location' not in tinfo:
                    tinfo['Location'] = '{}::/{}'.format(tinfo['Track Type'], tinfo['Persistent ID'])
            else:
                continue # Skip non audio files
            for f in ('Track Number', 'Year', 'Size'):
                if f not in tinfo:
                    tinfo[f] = None
            for f in ('Album', 'Artist', 'Name'):
                if f not in tinfo:
                    #tinfo[f] = 'Unknown {}'.format(f)
                    tinfo[f] = None
            tinfo['Total Time'] /= 1000
            row = {fields[k]:tinfo[k] for k in fields}
            yield row

    def createfieldmap(self):
        """Map of xml to winamp fields"""
        if self.xmlformat == 'plist':
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
            'Bit Rate': 'bitrate',
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
