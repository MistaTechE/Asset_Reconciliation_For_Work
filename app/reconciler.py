#reconciler.py
import pandas as pd


def build_current_assignments(checkouts_df: pd.DataFrame,
                              replacements_df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a DataFrame:
    State ID Number | State Tag (current device)
    """

    # Base assignments from checkouts
    current = checkouts_df[[
        "State ID Number",
        "State Tag Number"
    ]].copy()

    current = current.rename(columns={
        "State Tag Number": "Current State Tag"
    })
                                
    # Apply replacements (overwrite device per student)                                
    replacements_clean = replacements_df[[
      "State ID Number",
      "Replace Tag",
      "State Tag MB",
      "State Tag Media"
    ]].copy()
                                
    replacements_clean["Current State Tag"] = (
      replacements_clean["Replace Tag"]
      .fillna(replacements_clean["State Tag MB"])
      .fillna(replacements_clean["State Tag Media"])
    )

    replacements_clean = replacements_clean[[
      "State ID Number",
      "Current State Tag"
    ]].dropna()


    # Combine + keep latest (replacement wins automatically)
    combined = pd.concat([current, replacements_clean], ignore_index=True)

    # If a student has multiple entries, keep the last one (replacement overrides checkout)
    combined = combined.drop_duplicates(
        subset=["State ID Number"],
        keep="last"
    )

    return combined


def remove_returned_devices(assignments_df: pd.DataFrame,
                            returns_df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes any Chromebook or MacBook that appears in the returns list.
    """

    returned_tags = set(returns_df["State Tag Chromebook"].dropna())

    returned_tags.update(returns_df["State Tag MB"].dropna())

    filtered = assignments_df[~assignments_df["Current State Tag"].isin(returned_tags)].copy()

    return filtered
                              

def build_call_list(final_df: pd.DataFrame,
                    checkouts_df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds student + parent info back in.
    """

    enriched = final_df.merge(
        checkouts_df[
            [
                "State ID Number",
                "Student First Name",
                "Student Last Name",
                "Parents First Name",
                "Parents Last Name",
                "Parents Phone Number"
            ]
        ],
        on="State ID Number",
        how="left"
    )

    # Optional: cleaner output column
    enriched["Student Name"] = (
        enriched["Student First Name"] + " " + enriched["Student Last Name"]
    )

    enriched["Parent Name"] = (
        enriched["Parents First Name"] + " " + enriched["Parents Last Name"]
    )

    return enriched[[
        "State ID Number",
        "Student Name",
        "Parent Name",
        "Parents Phone Number",
        "Current State Tag"
    ]]


def reconcile(checkouts_df, replacements_df, returns_df):
    """
    Full pipeline entry point.
    """

    current_assignments = build_current_assignments(
        checkouts_df,
        replacements_df
    )

    not_returned = remove_returned_devices(
        current_assignments,
        returns_df
    )

    call_list = build_call_list(
        not_returned,
        checkouts_df
    )

    return call_list
