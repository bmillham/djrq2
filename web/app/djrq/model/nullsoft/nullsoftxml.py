from BeautifulSoup import BeautifulSoup
from datetime import datetime
import urllib
import sys
import htmllib

screen = sys.stdout

__author__="brian"
__date__ ="$Feb 6, 2011 1:38:17 AM$"

class MediaLibrary:
    """A class to read (not write) the xml created by winamp
       Tries to be as close to the nullsoftdb class as possible
    """
    
    def __init__(self, db='/home/brian/rond/Ronslist.xml', verbose=False, html=False):
        print "Reading the winamp xml"
        if html: print "<br>"
        self.xmlfile = db
        self.dbfields = {}
        self.fieldtypes = {}
        self.primaryindex = {}
        self.totalrecords = 0
        self.xmlformat = None
        self.encoding = None
        self.dfile = None
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
        self.dfile = open(self.xmlfile)
    
    def closedata(self):
        """Closes the data file"""
        self.dfile.close()
    
    def readheader(self):
        """Reads the header of the XML and figures out if it's a EZPLAYLIST or
           and Apple playlist export"""
        print "Reading header"
        if self.html: print "<br>"
        line = 1
        for l in self.dfile:
            lbs = BeautifulSoup(l)
            dtype = lbs.find('plist')
            ez = lbs.find('ezplaylist')
            if dtype or ez: break
            line += 1
            if line > 10: break

        if not dtype and not ez:
            print "Failed to find a header!"
        elif dtype:
            print "XML is Apple format"
            self.xmlformat = "apple"
            self.encoding = 'utf-8'
        elif ez:
            print "XML is EZPLAYLIST format"
            self.xmlformat = "ez"
            self.encoding = 'ISO=8859-1'
        if self.html: print "<br>"
        
    def readindex(self):
        """Read the indexes from the xml"""
        if self.html:
            print("<table border='1'><tr><th colspan='16'>")
        print "Finding indexes. This may take a while"
        if self.html:
            print "</th></tr>"
        icount = 0
        ix = 0
        if self.xmlformat == 'ez':
            self.dfile.seek(0)
        self.dfile.seek(0)
        offset = self.dfile.tell()
        tcells = 0
        while 1:
            l = self.dfile.readline()
            if not l: break
            lbs = BeautifulSoup(l)
            if self.xmlformat == 'ez':
                key = lbs.find('mediafile')
                if key is not None:
                    ix = icount
                    icount += 1
                    self.primaryindex[ix] = offset
                    if not ix % 250:
                        if tcells == 0 and self.html:
                            print "<tr><td>Index</td>"
                        if self.html: print "<td>"
                        screen.write('\r%s' % ix)
                        if self.html: print "</td>"
                        tcells += 1
                        if tcells == 15 and self.html:
                            tcells = 0
                            print "</tr>"
                        screen.flush()
            else:
                key = lbs.find('key')
                if key is not None:
                    k = key.string
                    if k == 'Playlists':
                        break
                    if k == 'Track ID':
                        val = lbs.find('integer')
                        ix = int(val.string)
                        self.primaryindex[ix] = offset
                        icount += 1
                        if not icount % 250:
                            if tcells == 0 and self.html:
                                print "<tr><td>Index</td>"
                            if self.html: print "<td>"
                            screen.write('\r%s' % ix)
                            screen.flush()
                            if self.html: print "</td>"
                            tcells += 1
                            if tcells == 15 and self.html:
                                tcells = 0
                                print "</tr>"
            offset = self.dfile.tell()
                
        self.totalrecords = len(self.primaryindex)
        if self.html:
            while tcells < 15:
                print("<td>&nbsp;</td>")
                tcells += 1
            print("</tr>") 
            print("<tr><th colspan='16'>")
        print "\nDone Reading %s indexes" % self.totalrecords
        if self.html: print "</th></td></table>"
        
    def fetchall(self):
        """Read all the records from the winamp xml"""
        for i in self.primaryindex:
            row = self.fetchone(i)
            yield row
    
    def fetchone(self, idx):
        """Reads a single record from the winamp xml"""
        if idx not in self.primaryindex:
            print "\nIndex %s is not a primary index" % idx
            return None

        self.dfile.seek(self.primaryindex[idx])
        pos = self.dfile.tell()
        if pos != self.primaryindex[idx]:
            print "ERROR: Failed to seek to index %s - %s!" % (idx, self.primaryindex['idx'])
            return None
        if self.xmlformat == 'apple':
            record = self.__fetchoneapple(idx)
        else:
            record = self.__fetchoneez(idx)
        return record
    
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
             'artist': 'artist',
             'title': 'title',
             'year': 'year',
             'album': 'album',
             'bitrate': 'bitrate',
             'time': 'length',
             'size': 'filesize',
             'filename': 'filename',
             'track': 'trackno',
             'lastmodified': 'lastmodified',
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
            print "Failed to convert date: ", d
        return date
    
    def rowtemplate(self):
        """Creates a blank row"""
        rowtemplate = {} # Create a blank row template, with all the keys
        for f in self.fieldmap.values():
            rowtemplate[f] = None
        
        return rowtemplate
    
    def unescape(self, s):
        """Decodes &amp; style encoding"""
        # EZ format has invalid &apos; chars. Fix it.
        s = s.replace('&apos;', '&#39;')
        p = htmllib.HTMLParser(None)
        p.save_bgn()
        p.feed(s)
        return p.save_end()
