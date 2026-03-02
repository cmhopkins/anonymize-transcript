# Identify everyone's initials to replace
# Create dictionary of names

import pandas as pd
import re
import sys

def create_at_dict(attendees_file):
    at_dict = {}

    df = pd.read_csv(attendees_file)
    df["Inits"] = df["First Name"].str[0] + df["Last Name"].str[0]
    df = df.drop(columns = ["Last Name", "Email", "Role", "Join Time", "Leave Time"])

    for _, row in df.iterrows():
        variants = [row["Full Name"], row["First Name"]]
        for variant in variants:
            at_dict[variant] = row["Inits"]
    return at_dict   

def anonymize(tf, attendees):
    with open(tf, "r", encoding="utf-8") as f:
        transcript = f.read()


    trans, _ = re.subn(r'\b(?:' + '|'.join(attendees.keys()) + r')\b', lambda match: attendees[match.group()], transcript)

    with open("stripped_transcript.txt", "w", encoding="utf-8") as f:
        f.write(trans)
            

def main(transcript_file, attendees_file):
    # Initialize dict of attendee names and anonymization aliases
    at_dict = create_at_dict(attendees_file)

    # Create anonymized/stripped version of transcript file
    anonymize(transcript_file, at_dict)
    
main("transcript.txt", "attendees.csv")
