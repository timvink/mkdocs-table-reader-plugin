# Consider alternatives

This plugin is built to be able to quickly insert table files anywhere in a markdown file. 

You could also consider alternative approaches that might fit your use-case better.

## Write tables to markdown files 

You could write a script (maybe triggered by a [mkdocs hook](https://www.mkdocs.org/user-guide/configuration/#hooks)) that writes the tables you need into markdown files. It could look something like this:

```python
# write markdown tables
import pandas as pd

md = pd.read_csv("your_file.csv").to_markdown()
with open("docs/assets/tables/my_file.md", "w") as f:
    f.write(md)
```

You can then use the [snippets extension](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/) to insert the tables into your markdown pages:

```md
# some_page.md

My table:

;--8<-- "assets/tables/my_file.md"
```

Upsides:

- Easy, fast, low on dependencies
- You can see changes of your tables in version control

Downsides:

- You need to generate/update the markdown files on every build
- if you move the page you have to update the path (if you used a relative path for the snippet)

## Execute python during build

You could also choose to insert the markdown for tables dynamically, using packages like [markdown-exec](https://pypi.org/project/markdown-exec/).

For example:

````
```python exec="true"
import pandas as pd

file_path = "path/to/file/from/project/root"
print(pd.read_csv(file_path).to_markdown(index=False, disable_numparse=True))
```
````

