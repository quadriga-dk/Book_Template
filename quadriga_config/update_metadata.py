#!/usr/bin/env python3
import yaml
import json
import re
from pathlib import Path

def update_metadata():
    # Load CITATION.cff
    with open('CITATION.cff', 'r') as f:
        citation_data = yaml.safe_load(f)
    print(citation_data["preferred-citation"])

if __name__ == "__main__":
    update_metadata()