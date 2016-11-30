# encoding: cinje

: def uploadheader sharetype
 : if sharetype == 'private'
    <h1>Your Private Files</h1>
    <blockquote>
        Click on 'Add Files' to select the files you would like to upload, or drag & drop them.
        If you use the winamp media library, send the contents of the ml directory (main.idx and main.dat). Otherwise, export to XML (either EZPLAYLIST or Apple format) and upload that. You may compress the files using zip, rar or gz.
        When your ml or xml files are uploaded, click on 'Update Your Database' in the menu to start updating your database
    </blockquote>
 : elif sharetype == 'shared'
    <h1>Your Files Shared With DJs</h1>
    <blockquote>
     Click on 'Add Files' to select the files you would like to upload, or drag & drop them.
     This area is shared between all DJs. Please respect each other, and do not delete files, unless they are yours!
    </blockquote>
 : end
: end
