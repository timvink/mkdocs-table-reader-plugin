# Test page

## read_parquet

{{ read_parquet('assets/tables/table.parquet') }}

## read_stata

{{ read_stata('assets/tables/table.dta') }}

## read_sas

{{ read_sas('assets/tables/table.xpt', encoding='utf-8') }}

## read_xml

{{ read_xml('assets/tables/table.xml', parser='etree') }}
