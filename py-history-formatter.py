#!/usr/bin/env python3
## py-history-forematter.py

import json
from collections import defaultdict

def parse_pressure_line(line: str):
    line = line.strip()
    if not line:
        return None
    parts = line.split("|")
    if len(parts) != 4:
        return None
    station_id, station_name, state_district_key, values_str = parts
    values = [v.strip() for v in values_str.split(",")]
    return station_id.strip(), station_name.strip(), state_district_key.strip(), values

def all_missing(values):
    return all(v in ("", "-") for v in values)

def fmt_values(values):
    return "-" if all_missing(values) else ", ".join(values)

def format_pressure_history(pressure_path, district_title_path_json):
    with open(district_title_path_json, "r", encoding="utf-8") as f:
        district_titles = json.load(f)

    grouped = defaultdict(lambda: defaultdict(list))
    with open(pressure_path, "r", encoding="utf-8") as f:
        for line in f:
            parsed = parse_pressure_line(line)
            if not parsed:
                continue
            station_id, station_name, state_district_key, values = parsed
            state = state_district_key.split("_", 1)[0]  # VIC/NSW/QLD...
            grouped[state][state_district_key].append((station_name, station_id, values))

    out = []
    for state in sorted(grouped.keys()):
        out.append(state)
        out.append("")

        for state_district_key in sorted(grouped[state].keys()):
            title = district_titles.get(state_district_key, state_district_key)
            out.append(f"  {state_district_key} - {title}")

            for station_name, station_id, values in sorted(
                grouped[state][state_district_key],
                key=lambda x: (x[0].lower(), x[1].lower())
            ):
                out.append(f"    {station_name} ({station_id}) : {fmt_values(values)}")

            out.append("")

        if out and out[-1] == "":
            out.pop()
        out.append("")

    return "\n".join(out).rstrip() + "\n"

if __name__ == "__main__":
    print(format_pressure_history("pressure_history.txt", "bom_weather.config.json"))
