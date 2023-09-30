import csv
from collections import defaultdict


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


def print_dept_stats(dept_stats: dict) -> None:
    """
    Print salary statistics for each department from a department-salary statistics dict.

    Args:
        dept_stats (dict): A dictionary representing the salary statistics for each department.
    """
    print('----Salary stats for each department----')

    for dept in dept_stats:
        dept_salaries = [float(sal) for sal in dept_stats[dept]]
        print(
            f'{dept}\n'
            f'\tWorkers number = {len(dept_salaries)}\n'
            f'\tAverage salary = {sum(dept_salaries) / len(dept_salaries):.2f} '
            f'({min(dept_salaries)} — {max(dept_salaries)})'
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
    Extract aggregated data from agg_col for each groupby_col from a CSV file and return them as a dictionary.

    Args:
        filepath (str, optional): The path to the CSV file (default 'data/Corp_Summary.csv').
        sep (str, optional): The separator used in the CSV file (default ';').
        encoding (str, optional): The encoding of the CSV file (default 'utf-8').
        groupby_col (int, optional): The column index to group by (default 0).
        agg_col (int, optional): The column index to aggregate (default 1).
        header (bool, optional): Whether the CSV file has a header row (default True).
        keep_duplicates (bool, optional): Whether to keep duplicate values in the aggregation (default True).

    Return:
        dict[str, list]: A dictionary representing the aggregated statistics with groupby values as keys.
    """
    stats = defaultdict(list)

    try:
        with open(filepath, encoding=encoding) as file:
            csv_reader = csv.reader(file, delimiter=sep)
            next(csv_reader) if header else None

            for row in csv_reader:
                if keep_duplicates:
                    stats[row[groupby_col]].append(row[agg_col])
                elif row[agg_col] not in stats[row[groupby_col]]:
                    stats[row[groupby_col]].append(row[agg_col])
    except Exception as e:
        print(f"An error occurred while processing the file: {str(e)}")

    return stats


def save_dept_stats_to_csv(
        dept_stats: dict,
        output_filepath='data/out_dept_stats.csv'
) -> None:
    """
    Save department salary statistics to a CSV file.

    Args:
        dept_stats (dict): A dictionary representing the salary statistics for each department.
        output_filepath (str, optional): The path to the output CSV file (default 'data/out_dept_stats.csv').
    """
    with open(output_filepath, 'w', newline='', encoding='UTF-8') as out_file:
        fieldnames = ['department', 'emp_cnt', 'max_sal', 'min_sal', 'avg_sal']
        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()

        for dept, salaries in dept_stats.items():
            dept_salaries = [float(sal) for sal in salaries]
            writer.writerow({
                'department': dept,
                'emp_cnt': len(dept_salaries),
                'max_sal': max(dept_salaries),
                'min_sal': min(dept_salaries),
                'avg_sal': sum(dept_salaries) / len(dept_salaries)
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
            dept_stats = get_csv_agg_stats(groupby_col=1, agg_col=5, keep_duplicates=True)
            print_dept_stats(dept_stats)
        elif choice == '3':
            dept_stats = get_csv_agg_stats(groupby_col=1, agg_col=5, keep_duplicates=True)
            save_dept_stats_to_csv(dept_stats)
            print("Summary report successfully saved to a CSV file.")
        elif choice == '4':
            print("Thank you for using the program!")
            break
        else:
            print("Invalid choice. Please select a valid action number.")
