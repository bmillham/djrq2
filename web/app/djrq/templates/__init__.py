""" Common class/style used on tables """
table_class = ['table',
               'table-bordered',
               'table-striped',
               'vertical-table',
              ]
table_style = ['margin-left: auto;',
               'margin-right: auto;',
               'width: auto;',
              ]

table_args = "class='{}' style='{}'".format(' '.join(table_class), ' '.join(table_style))
caption_args = "class='h3' style='text-align: center;'"
