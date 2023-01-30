# Test page

This test is related to this issue: https://github.com/timvink/mkdocs-table-reader-plugin/issues/29

## Table with pipes escaped

Basically `\|`

{{ read_csv("example_escaped.csv") }}


## Table with pipes unescaped

Basically just `|`

{{ read_csv("example_unescaped.csv", sep=",", engine="c") }}