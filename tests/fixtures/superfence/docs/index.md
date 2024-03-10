# site title


{{ read_csv('assets/tables/basic_table.csv') }}

```tablereader
filepath: /workspaces/mkdocs-table-reader-plugin/tests/fixtures/superfence/assets/tables/basic_table.csv
reader: read_csv
```

This one should fail (typo in reader value)

<!-- ```tablereader
filepath: assets/tables/basic_table.csv
reader: read_cvs
``` -->

This one should fail (typo in path)

<!-- ```tablereader
filepath: table.csv
reader: read_csv
``` -->

## An HTML table

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>col1</th>
      <th>col2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>3</td>
    </tr>
  </tbody>
</table>