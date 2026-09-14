# Changelog

Releases before 4.0.1 are described in the [GitHub releases](https://github.com/timvink/mkdocs-table-reader-plugin/releases).

## 4.0.1

Bug fixes:

- Two reader tags on the same line are now two tables. The tag pattern matched greedily, so it swallowed everything between the first and the last tag on a line, and then failed to parse the result.
- An `=` inside an argument value no longer breaks parsing. `{{ read_csv('a=b.csv') }}`, `sep='='` and `na_values=['a=1']` all raised a `SyntaxError` before.
- A comma inside a dict argument no longer breaks parsing, so `dtype={'a': 'str', 'b': 'int'}` works. Lists and tuples already worked.
- `convert_to_md_table()` no longer escapes pipe characters in the DataFrame you pass in. When a `mkdocs-macros-plugin` user rendered the same DataFrame twice, the second table showed doubly escaped pipes.

Project maintenance:

- The documentation site now deploys on every push to `master`. It was deployed by hand, and had fallen behind the readers added in 4.0.0.
- Coverage is uploaded to Codecov again. The upload step tested an environment variable that was never set, so it never ran.
- `enabled` is included in `schema.json`, so editors stop flagging it as an unknown option.
