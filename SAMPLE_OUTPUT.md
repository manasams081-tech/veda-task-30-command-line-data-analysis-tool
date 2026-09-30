# Sample Output — Task 30

## Help

```text
python cli_tool.py --file sample_data/sales.csv --summary
```

## Summary

```text
VEDA DATASET SUMMARY
====================
Rows              : 20
Columns           : 6
Missing values    : 0
Numeric columns   : units, sales
Column names      : date, region, product, units, sales, customer_type
```

## Statistics

```text
python cli_tool.py --file sample_data/sales.csv --stats sales
```

The command prints count, mean, median, minimum, maximum, standard deviation and total sales.

## Grouping

```text
python cli_tool.py --file sample_data/sales.csv --group region --metric sales
```

The result contains count, sum, mean, minimum and maximum sales per region.
