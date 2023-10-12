### One line web scraping by combining pandas and BeautifulSoup4

##### Check out the video

<div align="left">
      <a href="https://www.youtube.com/watch?v=pvnODvnMyrg">
         <img src="https://img.youtube.com/vi/pvnODvnMyrg/0.jpg" style="width:100%;">
      </a>
</div>

##### Code from the video

```python
pip install a-pandas-ex-bs4df 
```

```python
from a_pandas_ex_bs4df import pd_add_bs4_to_df
import pandas as pd
pd_add_bs4_to_df()    

from PrettyColorPrinter import add_printer #optional
add_printer(True) #optional

df=pd.Q_bs4_to_df(r'https://github.com/search?l=Python&q=python&type=Repositories')
df.loc[(~df.bb_href.isna()) & df.aa_attrs_values.str.contains('middle',regex=False, na=False)]
df.loc[(~df.bb_href.isna()) & df.aa_attrs_values.str.contains('middle',regex=False, na=False)].ff_fetchParents.apply(lambda x: x())
df.loc[(~df.bb_src.isna()) & (~df.bb_src.str.contains(r'\.png$',regex=True,na=False))]
df.loc[(~df.bb_src.isna()) & (df.bb_src.str.contains(r'\.png$',regex=True,na=False))]
```

```python
Parameters:
    htmlcode:Union[str,bytes]
        file path, url or html source code
        urls will be downloaded with requests
    dontuse:tuple
        bs4 attributes to exclude from the dataframe
        default = (
        "element_classes",
        "builder",
        "is_xml",
        "known_xml",
        "_namespaces",
        "parse_only",
        "markup",
        "contains_replacement_characters",
        "original_encoding",
        "declared_html_encoding",
        "parser_class",
        "namespace",
        "prefix",
        "cdata_list_attributes",
        "preserve_whitespace_tag_stack",
        "open_tag_counter",
        "preserve_whitespace_tags",
        "interesting_string_types",
        "current_data",
        "string_container_stack",
        "_most_recent_element",
        "currentTag",
    )
    parser: str
        Have a look at the bs4 documentation
        (default='lxml')
    tags_to_find:Union[bool,str]=True
        will be passed to soup.find_all()
        Have a look at the bs4 documentation
        (default=True) #everything
Returns:
    df: pd.DataFrame
```
