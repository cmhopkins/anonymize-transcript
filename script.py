# Identify everyone's initials to replace
# Create dictionary of names

import pandas as pd
import sys

def create_at_dict(attendees_file):
    at_dict = {}

    df = pd.read_csv(attendees_file)
    df["Inits"] = df["First Name"].str[0] + df["Last Name"].str[0]
    keys = df["Inits"]
    df = df.drop(columns = ["Last Name", "Email", "Role", "Join Time", "Leave Time"])

    for _, row in df.iterrows():
        variants = [row["Full Name"], row["First Name"]]
        for variant in variants:
            at_dict[variant] = row["Inits"]
    return at_dict   

def anonymize(tf, attendees):
    tf_obj = open(tf, "r")
    transcript = tf_obj.read()
    for name in sorted(attendees, key=len, reverse=True):
        transcript = transcript.replace(name, attendees[name])
    stripped = open('stripped_transcript.txt', 'w')
    stripped.write(transcript + '\n')
    stripped.close()
            

def main(transcript_file, attendees_file):
    # Initialize dict of attendee names and anonymization aliases
    at_dict = create_at_dict(attendees_file)

    # Create anonymized/stripped version of transcript file
    anonymize(transcript_file, at_dict)
    
main("transcript.txt", "attendees.csv")
