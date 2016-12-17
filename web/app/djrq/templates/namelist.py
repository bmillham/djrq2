# encoding: cinje
: from urllib.parse import quote_plus
: from . import table_args, caption_args

: def namelist ctx, names, columns=3
    <div class='container'>
     <div class='table-responsive'>
     <table #{table_args}>
    : resource = ctx.resource.__resource__
      <caption #{caption_args}>Browsing by ${resource.capitalize()}: ${ctx.selected_letter} <span class='label label-info'>${names.count()}</span></caption>
      <tbody>
        : row_ended = False
        : for i, name in enumerate(names)
            : if not (i % columns)
                : row_ended = False
                <tr>
            : end
            <td>
             <a href="/${resource}/?id=#{quote_plus(str(name.aid))}">${name.fullname}</a>&nbsp;<span class="badge pull-right">${name.songcount}</span>
            </td>
            : if i % columns == columns - 1
                : row_ended = True
                </tr>
             : if not int(i / columns) % 14 and i > columns
                </tbody>
                : flush
                <tbody>
             : end
            : end
        : end
        : if not row_ended
            : while i % columns != columns - 1 and i > columns - 1
                <td>&nbsp;</td>
                : i += 1
            : end
            </tr>
        : end
        </tbody>
     </table>
     </div>
    </div>
: end
