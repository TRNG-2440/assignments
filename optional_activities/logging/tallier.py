"""
tallier.py

Responsible for tallying validated votes into per-candidate totals.

Iterates over the validated vote list, incrementing a counter for
each candidate. Debug-level logging records each individual vote as
it is counted; info-level logging records the final tally.

This module is part of the Voting System Simulator logging activity.
Do not add or modify any logging calls in this file.
"""

import logging

logger = logging.getLogger(__name__)


def tally_votes(
    valid_votes: list[str],
    candidates: list[str],
) -> dict[str, int]:
    """
    Counts the number of votes received by each candidate.

    All candidates are included in the result even if they received
    zero votes, so the output always reflects the full candidate field.

    Args:
        valid_votes (list[str]): Validated vote strings from the validator.
        candidates (list[str]): Full list of candidates standing in the election.

    Returns:
        dict[str, int]: Mapping of candidate name to vote count.
    """
    logger.info("Starting vote tally for %d valid vote(s).", len(valid_votes))

    tally = {candidate: 0 for candidate in candidates}

    for vote in valid_votes:
        tally[vote] += 1
        logger.debug(
            "Counted vote for '%s'. Running total: %d.",
            vote,
            tally[vote],
        )

    for candidate, count in sorted(tally.items(), key=lambda x: x[1], reverse=True):
        logger.info("  %-20s %d vote(s)", candidate, count)

    logger.info("Tally complete. Total valid votes counted: %d.", len(valid_votes))

    return tally
