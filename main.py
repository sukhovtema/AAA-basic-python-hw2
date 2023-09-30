import csv


def print_dept_teams_hierarchy(dept_teams_hierarchy: dict) -> None:
    """
    Print department-teams hierarchy from a department-teams hierarchy dictionary.

    Args:
        dept_teams_hierarchy (dict): A dictionary representing the department-teams hierarchy.
    """
    print('----Department-Teams hierarchy----')

    for dept in dept_teams_hierarchy:
        print(dept)
        for dept_team in dept_teams_hierarchy[dept]:
            print(f'\t{dept_team}')


def print_dept_sal_stats(dept_sal_stats: dict) -> None:
    """
    Print salary statistics for each department from a salary statistics for each department dict.

    Args:
        dept_sal_stats (dict): A dictionary representing the salary statistics for each department.
    """
    print('----Salary stats for each department----')

    for dept in dept_sal_stats:
        dept_sal_arr = [int(sal) for sal in dept_sal_stats[dept]]
        print(
            f'{dept}\n'
            f'\tMAX_SAL = {max(dept_sal_arr)}\n'
            f'\tMIN_SAL = {min(dept_sal_arr)}\n'
            f'\tAVG_SAL = {sum(dept_sal_arr) / len(dept_sal_arr):.2f}'
        )


def get_csv_agg_stats(
        filepath: str = 'data/Corp_Summary.csv',
        sep: str = ';',
        encoding: str = 'utf-8',
        groupby_col: int = 0,
        agg_col: int = 1,
        header: bool = True,
        keep_duplicates: bool = True
) -> dict:
    """
    Extract aggregated statistics from a CSV file and return them as a dictionary.

    Args:
        filepath (str, optional): The path to the CSV file (default 'data/Corp_Summary.csv').
        sep (str, optional): The separator used in the CSV file (default ';').
        encoding (str, optional): The encoding of the CSV file (default 'utf-8').
        groupby_col (int, optional): The column index to group by (default 0).
        agg_col (int, optional): The column index to aggregate (default 1).
        header (bool, optional): Whether the CSV file has a header row (default True).
        keep_duplicates (bool, optional): Whether to keep duplicate values in the aggregation (default True).

    Return:
        dict: A dictionary representing the aggregated statistics with groupby values as keys.
    """
    stats = {}

    try:
        with open(filepath, encoding=encoding) as file:
            csv_reader = csv.reader(file)
            # skip header if exists
            next(csv_reader) if header else None

            for row in csv_reader:
                row_parts = row[0].split(sep)
                if row_parts[groupby_col] in stats:
                    if keep_duplicates:
                        stats[row_parts[groupby_col]].append(row_parts[agg_col])
                    elif row_parts[agg_col] not in stats[row_parts[groupby_col]]:
                        stats[row_parts[groupby_col]].append(row_parts[agg_col])
                else:
                    stats[row_parts[groupby_col]] = [row_parts[agg_col]]
    except Exception as e:
        print(f"An error occurred while processing the file: {str(e)}")

    return stats


def save_dept_sal_stats_to_csv(
        dept_sal_stats: dict,
        output_filepath='data/out_dept_sal_stats.csv'
) -> None:
    """
    Save department salary statistics to a CSV file.

    Args:
        dept_sal_stats (dict): A dictionary representing the salary statistics for each department.
        output_filepath (str, optional): The path to the output CSV file (default 'data/out_dept_sal_stats.csv').
    """
    with open(output_filepath, 'w', newline='', encoding='UTF-8') as out_file:
        fieldnames = ['Department', 'MAX_SAL', 'MIN_SAL', 'AVG_SAL']
        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()

        for dept, salaries in dept_sal_stats.items():
            dept_sal_arr = [int(sal) for sal in salaries]
            writer.writerow({
                'Department': dept,
                'MAX_SAL': max(dept_sal_arr),
                'MIN_SAL': min(dept_sal_arr),
                'AVG_SAL': sum(dept_sal_arr) / len(dept_sal_arr)
            })


if __name__ == '__main__':
    print('Welcome!')

    while True:
        print(
            "\nSelect an action:\n"
            "1. Print department-teams hierarchy\n"
            "2. Print summary report for departments\n"
            "3. Save summary report to CSV file\n"
            "4. Exit"
        )

        choice = input("Enter the action number: ")

        if choice == '1':
            dept_teams_hierarchy = get_csv_agg_stats(groupby_col=1, agg_col=2, keep_duplicates=False)
            print_dept_teams_hierarchy(dept_teams_hierarchy)
        elif choice == '2':
            dept_sal_stats = get_csv_agg_stats(groupby_col=1, agg_col=5, keep_duplicates=True)
            print_dept_sal_stats(dept_sal_stats)
        elif choice == '3':
            dept_sal_stats = get_csv_agg_stats(groupby_col=1, agg_col=5, keep_duplicates=True)
            save_dept_sal_stats_to_csv(dept_sal_stats)
            print("Summary report successfully saved to a CSV file.")
        elif choice == '4':
            print("Thank you for using the program!")
            break
        else:
            print("Invalid choice. Please select a valid action number.")
