import requests
import json

def send_update(ws, cp=None, rc=None, deletedtracks=None, deletedrequests=None, deletedplayed=None, deletedmistags=None, totaltracks=None, checkedtracks=None, field=None, filename=None, updatedcount=None, newcount=None, stage=None, avetime=None, active=None, spinner=None, updaterunning=None):
    d = {}
    if active is not None:
        d['active'] = active
    if cp is not None:
        d['progress'] = cp
    if deletedtracks is not None:
        d['deletedtracks'] = deletedtracks
    if deletedrequests is not None:
        d['deletedrequests'] = deletedrequests
    if deletedplayed is not None:
        d['deletedplayed'] = deletedplayed
    if deletedmistags is not None:
        d['deletedmistags'] = deletedmistags
    if totaltracks is not None:
        d['totaltracks'] = totaltracks
    if checkedtracks is not None:
        d['checkedtracks'] = checkedtracks
    if avetime is not None:
        d['avetime'] = '{:.5f}'.format(avetime)
    if field is not None:
        #d['difference'] = '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(rc['filename'], field, s[fieldmap[field]], rc[field])
        d['updatedcount'] = updatedcount
    if updatedcount is not None:
        d['updatedcount'] = updatedcount
    if stage is not None:
        d['stage'] = stage
    if newcount is not None:
        d['newcount'] = newcount
        #d['newtrack'] = '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(rc['filename'], rc['artist'], rc['album'], rc['title'])
    if spinner is not None:
        d['spinner'] = spinner
    if updaterunning is not None:
        d['updaterunning'] = updaterunning
    requests.post(ws, data=json.dumps(d))
