import pandas as pd

def read_traj_summary_file_as_dataframe(extracted_file_path: str):
    trajectory_df = pd.read_csv(extracted_file_path, engine='python', sep=r'\s*;\s*',
                                skiprows=[0, 5, 6],
                                header=[0, 1], na_values=['nan', '...', 'None'])
    # Clean header text
    trajectory_df.columns = trajectory_df.columns.map(
        lambda h: '{}{}'.format(_clean_header(h[0]), _clean_header(h[1], is_unit=True)))

    # Set data types
    trajectory_df['Beginning (UTC Time)'] = pd.to_datetime(trajectory_df['Beginning (UTC Time)'],
                                                           format='%Y-%m-%d %H:%M:%S')
    trajectory_df['IAU (code)'] = trajectory_df['IAU (code)'].astype(str)
    trajectory_df['Participating (stations)'] = trajectory_df['Participating (stations)'].astype(str)

    return trajectory_df

def _clean_header(text, is_unit=False):
    """
    Extract header text from the raw csv file headers.
    :param text: Raw csv header
    :param is_unit: Optionally return text with brackets for units
    :returns: Formatted text
    """

    # Return an empty string if there is no header found
    if "Unnamed" in text:
        return ""

    # Removes additional spaces and hashtags from text. Add brackets optionally.
    clean_header = " ".join(text.replace("#", "").split())
    if is_unit:
        clean_header = f" ({clean_header})"

    return clean_header