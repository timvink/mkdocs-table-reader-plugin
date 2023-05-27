# YAML

## read_yaml

The latest numbers using `read_yaml()`:

{{ read_yaml('assets/tables/yaml_table.yml') }}

## with a multi-line yaml

Note that mkdocs does not support multi-line cells in markdown tables, see https://github.com/timvink/mkdocs-table-reader-plugin/issues/47.

{{ read_yaml('assets/tables/multiline_yaml.yml') }}

## with URLs

See https://github.com/timvink/mkdocs-table-reader-plugin/issues/48

{{ read_yaml('assets/tables/with_links.yml') }}