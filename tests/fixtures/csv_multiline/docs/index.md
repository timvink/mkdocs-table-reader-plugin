# Test page

This test is related to this issue: https://github.com/timvink/mkdocs-table-reader-plugin/issues/83

## Table with a multiline cell

A cell containing newlines, which are rendered as `<br>`.

{{ read_csv("example_multiline.csv") }}
