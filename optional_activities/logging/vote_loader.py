"""
vote_loader.py

Responsible for reading raw vote entries from a plain text file.

Each line in the votes file represents a single vote and should contain
a candidate name. Leading/trailing whitespace is stripped from each entry,
including blank lines which are passed through as empty strings for the
validator to classify as spoiled ballots.

This module is part of the Voting System Simulator logging activity.
Do not add or modify any logging calls in this file.
"""

import logging

logger = logging.getLogger(__name__)


def load_votes(filepath: str) -> list[str]:
    """
    Reads a votes file and returns a list of raw vote strings.

    Every line in the file is treated as one vote entry. Whitespace is
    stripped, but blank lines are returned as empty strings rather than
    being dropped — the validator is responsible for classifying them
    as spoiled ballots. No other validation is performed here.

    Args:
        filepath (str): Path to the plain text votes file.

    Returns:
        list[str]: Raw vote strings, one per line (including empty strings for blank lines).

    Raises:
        FileNotFoundError: if the file does not exist at the given path.
        IOError: if the file cannot be read.
    """
    logger.info("Attempting to load votes from '%s'.", filepath)

    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        logger.error("Votes file not found: '%s'.", filepath)
        raise
    except IOError as e:
        logger.error("Failed to read votes file '%s': %s", filepath, e)
        raise

    raw_votes = [line.strip() for line in lines]

    logger.info(
        "Successfully loaded %d vote(s) from '%s'.",
        len(raw_votes),
        filepath,
    )

    return raw_votes
