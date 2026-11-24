// See https://squidfunk.github.io/mkdocs-material/reference/data-tables/#sortable-tables

app.document$.subscribe(function() {
  var tables = document.querySelectorAll("article table")
  tables.forEach(function(table) {
    new Tablesort(table)
  })
})
