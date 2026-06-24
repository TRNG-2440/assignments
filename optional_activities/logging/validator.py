"""
validator.py

Responsible for validating raw vote entries against a known candidate list.

Each vote is checked for two failure conditions:
  - Empty or whitespace-only strings (spoiled ballots)
  - Names that do not match any known candidate (invalid votes)

Valid votes are returned as a list. Invalid and spoiled votes are
logged as warnings and excluded from the output.

This module is part of the Voting System Simulator logging activity.
Do not add or modify any logging calls in this file.
"""

import logging

logger = logging.getLogger(__name__)


def validate_votes(
    raw_votes: list[str],
    candidates: list[str],
) -> list[str]:
    """
    Validates a list of raw vote strings against an accepted candidate list.

    Comparison is case-insensitive. Valid votes are returned normalised to
    the original casing defined in the candidates list.

    Args:
        raw_votes (list[str]): Raw vote strings from the loader.
        candidates (list[str]): List of accepted candidate names.

    Returns:
        list[str]: Only the valid vote strings, normalised to candidate casing.
    """
    logger.info(
        "Beginning validation of %d vote(s) against %d candidate(s): %s.",
        len(raw_votes),
        len(candidates),
        ", ".join(candidates),
    )

    candidate_map = {c.lower(): c for c in candidates}
    valid_votes = []
    invalid_count = 0
    spoiled_count = 0

    for i, vote in enumerate(raw_votes, start=1):
        if not vote:
            spoiled_count += 1
            logger.warning(
                "Vote #%d is a spoiled ballot (empty entry) — excluded from tally.",
                i,
            )
            continue

        normalised = vote.lower()
        if normalised not in candidate_map:
            invalid_count += 1
            logger.warning(
                "Vote #%d is invalid — '%s' does not match any known candidate. "
                "Known candidates: %s.",
                i,
                vote,
                ", ".join(candidates),
            )
            continue

        valid_votes.append(candidate_map[normalised])
        logger.info("Vote #%d accepted: '%s'.", i, candidate_map[normalised])

    logger.info(
        "Validation complete — %d valid, %d invalid, %d spoiled.",
        len(valid_votes),
        invalid_count,
        spoiled_count,
    )

    return valid_votes
