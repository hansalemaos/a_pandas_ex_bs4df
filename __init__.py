import os
from functools import partial
from typing import Union

import bs4
import pandas as pd
import regex
import requests
from useful_functions_easier_life import NamedFunction


def get_soup_df(
    htmlcode: Union[str, bytes],
    dontuse: tuple = (
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
    ),
    parser: str = "lxml",
    tags_to_find: Union[bool, str] = True,
) -> pd.DataFrame:
    r"""
    from a_pandas_ex_bs4df import pd_add_bs4_to_df
    import pandas as pd
    pd_add_bs4_to_df()

    df=pd.Q_bs4_to_df(r'https://github.com/search?l=Python&q=python&type=Repositories')
    df.loc[(~df.bb_href.isna()) & df.aa_attrs_values.str.contains('middle',regex=False, na=False)]
    df.loc[(~df.bb_href.isna()) & df.aa_attrs_values.str.contains('middle',regex=False, na=False)].ff_fetchParents.apply(lambda x: x())
    df.loc[(~df.bb_src.isna()) & (~df.bb_src.str.contains(r'\.png$',regex=True,na=False))]
    df.loc[(~df.bb_src.isna()) & (df.bb_src.str.contains(r'\.png$',regex=True,na=False))]
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
    """

    def get_values_from_soup(key, aa_attrs_backup):
        val = aa_attrs_backup.get(key)
        if val is None:
            return pd.NA
        if isinstance(val, list):
            val = " ".join(val).strip()
        return val

    def get_soup_fuctions(soupobjekt):
        all_functions = []
        all_functions_name = []
        for x in soupobjekt.__dir__():
            if not x.startswith("_"):
                if callable(getattr(soupobjekt, x)):

                    funktion = NamedFunction(
                        name="",
                        execute_function=partial((getattr(soupobjekt, x))),
                        name_function=lambda: "()",
                        str_prefix="",
                        print_before_execution="",
                        str_suffix="",
                        ljust_prefix=0,
                        rjust_prefix=0,
                        ljust_suffix=0,
                        rjust_suffix=0,
                    )

                    all_functions.append(funktion)
                    all_functions_name.append(x)
        return pd.DataFrame([all_functions], columns=all_functions_name)

    def get_html_src(htmlcode):
        if isinstance(htmlcode, str):
            if os.path.exists(htmlcode):
                if os.path.isfile(htmlcode):
                    with open(htmlcode, mode="rb") as f:
                        htmlcode = f.read()
            elif regex.search(r"^.{1,10}://", str(htmlcode)) is not None:
                htmlcode = requests.get(htmlcode).content
        return htmlcode

    htmlcode = get_html_src(htmlcode)
    soup = bs4.BeautifulSoup(htmlcode, parser)
    htmlcodes = [
        pd.DataFrame(
            [("soup", soup)] + [x for x in soup.__dict__.items() if x[0] not in dontuse]
        ).set_index(0)
    ]
    htmlcodes.extend(
        [
            pd.DataFrame(
                [("soup", elem)]
                + [x for x in elem.__dict__.items() if x[0] not in dontuse]
            ).set_index(0)
            for elem in soup.find_all(tags_to_find)
        ]
    )
    df = pd.concat(htmlcodes, axis=1).T.copy()
    df.columns = [f"aa_{x}" for x in df.columns]
    df["aa_attrs_backup"] = df["aa_attrs"]
    df = df.reset_index(drop=True)
    df = (df.explode("aa_attrs")).copy()
    df["aa_attrs"] = df["aa_attrs"].fillna("")

    allnewcols = []
    for key in df.aa_attrs.drop_duplicates():
        if key == "":
            continue
        newcol = "bb_" + regex.sub("-", "_", key)
        allnewcols.append((key, newcol))
    for col in allnewcols:
        key = col[0]
        newcol = col[1]
        df[newcol] = df.apply(
            lambda x: get_values_from_soup(key=key, aa_attrs_backup=x.aa_attrs_backup),
            axis=1,
        )

    df["old_index"] = df.index
    df = (
        df.drop_duplicates(subset=["old_index"])
        .drop(columns="old_index")
        .reset_index(drop=True)
        .copy()
    )

    df2 = df.aa_soup.map(get_soup_fuctions)
    df3 = pd.concat(df2.to_list()).reset_index(drop=True)
    df3.columns = [f"ff_{x}" for x in df3.columns]
    df = pd.concat([df, df3], axis=1).copy()
    df["aa_attrs_keys"] = df.aa_attrs_backup.map(lambda x: "|".join(list(x)))
    df["aa_attrs_values"] = df["aa_attrs_backup"].map(
        lambda x: "|".join(([str(xx[1]) for xx in x.items()]))
    )
    df = df.drop(columns=["aa_attrs"]).copy()
    df = df.filter(sorted(df.columns)).copy()
    return df


def pd_add_bs4_to_df():
    pd.Q_bs4_to_df = get_soup_df
