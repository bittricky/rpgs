#!/usr/bin/env python3
import pandas as pd

def calculate_total_playtime():
    """Calculate total playtime hours from rpgs.csv"""
    df = pd.read_csv('rpgs.csv')
    total_hours = df['playtime'].sum()
    return total_hours

def generate_shield_badge():
    """Generate a shields.io badge URL with total playtime"""
    hours = calculate_total_playtime()
    return f"![Total Estimated Playtime](https://img.shields.io/badge/Total%20Estimated%20Playtime-{hours}%20hours-blue)"

if __name__ == '__main__':
    print(generate_shield_badge())
