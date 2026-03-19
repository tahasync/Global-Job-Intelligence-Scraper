import pandas as pd
import re
import os
from pathlib import Path

# Resolve paths relative to this script so it works from any working directory
BASE_DIR = Path(__file__).parent.parent

def analyze_jobs():
    file_path = BASE_DIR / 'data' / 'final' / 'jobs.csv'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} jobs.")

    # 1. Top skills appearing most often
    # Since explicit skills might be missing from JSON-LD, we extract from description.
    common_skills = [
        'Python', 'Java', 'JavaScript', 'React', 'Node.js', 'Node', 'C++', 'C#', 
        'SQL', 'AWS', 'Azure', 'HTML', 'CSS', 'Angular', 'Vue', 'Docker', 
        'Kubernetes', 'PHP', 'Django', 'Flask', 'Spring', 'REST', '.NET',
        'TypeScript', 'Git', 'Agile', 'Scrum'
    ]
    
    skill_counts = {skill: 0 for skill in common_skills}
    for desc in df['Job description'].dropna():
        # simple word match ignoring case
        desc_lower = desc.lower()
        for skill in common_skills:
            # use word boundaries for matching e.g. "C" or "Java"
            if re.search(r'\b' + re.escape(skill.lower()) + r'\b', desc_lower):
                skill_counts[skill] += 1
                
    top_skills = pd.Series(skill_counts).sort_values(ascending=False).head(10)

    # 2. City or region with the highest number of openings
    # Fill missing locations
    locations = df['Location'].fillna('Unknown').value_counts().head(5)

    # 3. Companies posting the highest number of relevant roles
    companies = df['Company name'].fillna('Unknown').value_counts().head(5)

    # 4. Count of internship, junior, or entry-level positions
    is_junior = df['Job title'].fillna('').str.contains('intern|junior|entry|trainee', case=False, na=False)
    entry_count = is_junior.sum()

    # 5. Most common job titles or role families
    titles = df['Job title'].fillna('Unknown').value_counts().head(5)

    # Generate Markdown Report
    os.makedirs(BASE_DIR / 'docs', exist_ok=True)
    with open(BASE_DIR / 'docs' / 'report.md', 'w') as f:
        f.write("# Rozee.pk Job Market Analysis Report\n\n")
        f.write("## Overview\n")
        f.write(f"Analyzed {len(df)} job postings from Rozee.pk.\n\n")

        f.write("## Top Skills in Demand\n")
        for skill, count in top_skills.items():
            if count > 0:
                f.write(f"- **{skill}**: {count} mentions\n")
        f.write("\n")

        f.write("## Top Cities for Openings\n")
        for loc, count in locations.items():
            f.write(f"- {loc}: {count} jobs\n")
        f.write("\n")

        f.write("## Top Hiring Companies\n")
        for comp, count in companies.items():
            f.write(f"- {comp}: {count} jobs\n")
        f.write("\n")

        f.write("## Entry-Level Opportunities\n")
        f.write(f"Found **{entry_count}** jobs catering to Interns, Juniors, or Entry-level professionals.\n\n")

        f.write("## Most Common Job Titles\n")
        for title, count in titles.items():
            f.write(f"- {title}: {count} posings\n")
        f.write("\n")

    print(f"Analysis saved to {BASE_DIR / 'docs' / 'report.md'}")

if __name__ == "__main__":
    analyze_jobs()
