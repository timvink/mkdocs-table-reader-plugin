# Test page

Files that are not UTF-8 encoded can be read by specifying the `encoding`:

## read_yaml

{{ read_yaml('assets/tables/cp1251_table.yml', encoding='cp1251') }}

## read_raw

{{ read_raw('assets/tables/cp1251_table.md', encoding='cp1251') }}
