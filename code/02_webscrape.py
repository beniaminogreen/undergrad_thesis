#!/usr/bin/env python
from scaling import recover_scores, repair_matrix
from in_region import in_region, to_wide
from between_regions import create_v_df, between_region
import tqdm as tqdm
import pickle as pkl
import pandas as pd

with open("data/dma_abbreviations.pkl", "rb") as f:
    dmas = pkl.load(f)

terms = ["nigger", "coon", "kike", "spic", "spook"]

for i, term in tqdm.tqdm(enumerate(terms)):
    in_region_dfs = tuple(
        in_region(term, dma, True, timeframe="all") for dma in tqdm.tqdm(dmas))
    wide_dfs = map(to_wide, in_region_dfs)
    h_df = pd.concat(wide_dfs).sort_index()

    dfs = tuple(
        create_v_df([term], year) for year in tqdm.tqdm(range(2004, 2021)))
    v_df = pd.concat(dfs, axis=1).sort_index()

    h_df = h_df.drop("2021", axis=1)
    v_matrix = v_df.to_numpy(copy=True)
    h_matrix = h_df.to_numpy(copy=True)

    gen1 = recover_scores(h_matrix, v_matrix)
    final = repair_matrix(h_matrix, v_matrix, gen1)
    final = pd.DataFrame(final)
    final.columns = h_df.columns
    final.index = h_df.index

    final.to_csv(f"data/scaled_word_{i+2}.csv")

old_df = None
for year in range(2004, 2021):

    timeframe = f"{year}-01-01 {year}-12-31"
    df = between_region(terms,
                        censor=False,
                        timeframe=timeframe,
                        geo="US",
                        gprop="")
    df['year'] = year

    old_df = pd.concat([old_df, df], axis=0)

old_df.rename(columns={
    old_df.columns[0]: "word1_weight",
    old_df.columns[1]: "word2_weight",
    old_df.columns[2]: "word3_weight",
    old_df.columns[3]: "word4_weight",
    old_df.columns[4]: "word5_weight"
},
              inplace=True)

old_df.to_csv("data/between_region_comparisons.csv")
