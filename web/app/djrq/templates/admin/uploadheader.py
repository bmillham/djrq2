# encoding: cinje

: def uploadheader sharetype
 : if sharetype == 'private'
    <h1>Your Private Files</h1>
    <blockquote>
        Click on 'Add Files' to select the files you would like to upload, or drag & drop them.
        <ul>
         <li>For Winamp users</li>
         <ul>
          <li>If you use the media library, send the contents of the ml directory (main.idx and main.dat)
          <li>If you do not use the media library, export to XML (EZPLAYLIST and Apple formats are accepted)
         </ul>
         <li>For iTunes users</li>
         <ul>
          <li>Send the iTunes XML file</li>
         </ul>
        </ul>
        After your files are uploaded, click on <a href='/admin/updatedatabase'>Update Database</a> in the menu to start updating your database.
    </blockquote>
 : elif sharetype == 'shared'
    <h1>Your Files Shared With DJs</h1>
    <blockquote>
     Click on 'Add Files' to select the files you would like to upload, or drag & drop them.
     This area is shared between all DJs. Please respect each other, and do not delete files, unless they are yours!
    </blockquote>
 : end
: end
