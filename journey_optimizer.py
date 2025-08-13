"""
Journey Analysis Optimizer for FastAPI Backend
Reduces redundant action_shelf_mapping data and generates journey analysis
"""

from collections import defaultdict
import pandas as pd
from typing import List, Dict, Tuple, Any

def deduplicate_action_shelf_mapping(action_shelf_mapping: List[List]) -> List[List]:
    """
    Remove consecutive duplicate entries from action_shelf_mapping
    Only keep transitions/changes in person-shelf-action combinations
    """
    if not action_shelf_mapping:
        return []
    
    deduplicated = []
    last_entry = None
    
    for entry in action_shelf_mapping:
        # Handle different data formats
        if len(entry) == 4:  # [pid, frame, shelf_id, action]
            pid, frame, shelf_id, action = entry
            current_key = (pid, shelf_id, action)
        elif len(entry) == 1:  # [action] only
            action = entry[0]
            current_key = (None, None, action)
        else:
            continue
        
        # Only add if different from last entry
        if current_key != last_entry:
            deduplicated.append(entry)
            last_entry = current_key
    
    return deduplicated

def generate_journey_analysis_optimized(action_shelf_mapping: List[List]) -> Dict[str, Any]:
    """
    Generate journey analysis directly from action_shelf_mapping data
    Similar to Gradio's generate_journey_analysis but optimized for FastAPI
    """
    if not action_shelf_mapping:
        return {}
    
    # Convert to DataFrame for easier processing
    valid_entries = []
    for entry in action_shelf_mapping:
        if len(entry) >= 4:  # Has all required fields
            valid_entries.append({
                'pid': entry[0],
                'frame': entry[1], 
                'shelf_id': entry[2],
                'action': entry[3]
            })
    
    if not valid_entries:
        return {}
    
    df = pd.DataFrame(valid_entries)
    
    # Find key events per person-shelf combination
    reach_events = df[df['action'] == 'Reach To Shelf'][['pid', 'shelf_id']].drop_duplicates().assign(did_reach=True)
    inspect_events = df[df['action'].isin(['Inspect Product', 'Inspect Shelf'])][['pid', 'shelf_id']].drop_duplicates().assign(did_inspect=True)
    return_events = df[df['action'] == 'Hand In Shelf'][['pid', 'shelf_id']].drop_duplicates().assign(did_return=True)
    
    # Create analysis dataframe
    interactions = df[['pid', 'shelf_id']].drop_duplicates()
    analysis_df = pd.merge(interactions, reach_events, on=['pid', 'shelf_id'], how='left')
    analysis_df = pd.merge(analysis_df, inspect_events, on=['pid', 'shelf_id'], how='left')
    analysis_df = pd.merge(analysis_df, return_events, on=['pid', 'shelf_id'], how='left')
    analysis_df = analysis_df.fillna(False)
    
    # Categorize outcomes
    def categorize_outcome(row):
        if not row['did_reach']:
            return 'No Reach'
        if row['did_inspect'] and row['did_return']:
            return 'Keraguan & Pembatalan'
        elif row['did_inspect'] and not row['did_return']:
            return 'Konversi Sukses'
        else:
            return 'Kegagalan Menarik Minat'
    
    analysis_df['outcome'] = analysis_df.apply(categorize_outcome, axis=1)
    relevant_outcomes = analysis_df[analysis_df['outcome'] != 'No Reach']
    
    if relevant_outcomes.empty:
        return {}
    
    # Aggregate results by shelf
    outcome_summary = relevant_outcomes.groupby(['shelf_id', 'outcome']).size().unstack(fill_value=0)
    outcome_percentage = outcome_summary.div(outcome_summary.sum(axis=1), axis=0) * 100
    
    # Ensure all outcome columns exist
    desired_order = ['Konversi Sukses', 'Keraguan & Pembatalan', 'Kegagalan Menarik Minat']
    for col in desired_order:
        if col not in outcome_percentage.columns:
            outcome_percentage[col] = 0
    
    outcome_percentage = outcome_percentage[desired_order]
    
    # Convert to format suitable for frontend
    journey_data = []
    for shelf_id, row in outcome_percentage.iterrows():
        journey_data.append({
            'shelf_id': shelf_id,
            'konversi_sukses': round(row['Konversi Sukses'], 1),
            'keraguan_pembatalan': round(row['Keraguan & Pembatalan'], 1),
            'kegagalan_menarik_minat': round(row['Kegagalan Menarik Minat'], 1),
            'total_interactions': int(outcome_summary.loc[shelf_id].sum())
        })
    
    return {
        'journey_analysis': journey_data,
        'total_person_shelf_interactions': len(relevant_outcomes),
        'outcome_distribution': {
            'konversi_sukses': len(relevant_outcomes[relevant_outcomes['outcome'] == 'Konversi Sukses']),
            'keraguan_pembatalan': len(relevant_outcomes[relevant_outcomes['outcome'] == 'Keraguan & Pembatalan']),
            'kegagalan_menarik_minat': len(relevant_outcomes[relevant_outcomes['outcome'] == 'Kegagalan Menarik Minat'])
        }
    }

def optimize_for_frontend(action_shelf_mapping: List[List]) -> Tuple[List[List], Dict[str, Any]]:
    """
    Main optimization function for frontend
    Returns deduplicated mapping and journey analysis
    """
    # Step 1: Deduplicate the raw data
    deduplicated_mapping = deduplicate_action_shelf_mapping(action_shelf_mapping)
    
    # Step 2: Generate journey analysis
    journey_analysis = generate_journey_analysis_optimized(action_shelf_mapping)
    
    return deduplicated_mapping, journey_analysis
