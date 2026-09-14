# Test page

Tables keep the indentation of their tag, so they can go inside components
that rely on indentation.

## Inside an admonition

!!! note "A note"

    {{ read_csv("basic_table.csv") }}

## Inside a content tab

=== "A tab"

    {{ read_csv("basic_table.csv") }}

## Without indentation

{{ read_csv("basic_table.csv") }}
