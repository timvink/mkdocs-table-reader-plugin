# Test page

## read_html

Inserts the first table in the file:

{{ read_html('assets/tables/table.html') }}

Use 'match' to select another table:

{{ read_html('assets/tables/table.html', match='second_html_table') }}

## read_xml

{{ read_xml('assets/tables/table.xml') }}
