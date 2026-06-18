"""
results_reporter.py

Responsible for determining the election outcome from the final tally
and reporting the result.

Outcome logic:
  - If two or more candidates share the highest vote count, the result
    is a tie and an error is logged.
  - If the winner's margin over the runner-up is within the defined
    narrow-margin threshold, a warning is logged.
  - Otherwise, the winner is announced at INFO level.

This module is part of the Voting System Simulator logging activity.
Do not add or modify any logging calls in this file.
"""

import logging

logger = logging.getLogger(__name__)

# A winning margin at or below this percentage of total votes
# is considered narrow and triggers a warning.
NARROW_MARGIN_THRESHOLD_PCT = 5.0


def report_results(tally: dict[str, int]) -> dict:
    """
    Determines the election outcome from a completed tally and logs the result.

    Args:
        tally (dict[str, int]): Mapping of candidate name to vote count,
                                as returned by tallier.tally_votes().

    Returns:
        dict: Outcome dict with keys:
                'status'    : 'winner', 'tie', or 'no_votes'
                'winner'    : winning candidate name, or None
                'tally'     : the full tally dict
                'margin'    : vote margin between winner and runner-up, or None
                'margin_pct': margin as a percentage of total votes, or None
    """
    total_votes = sum(tally.values())

    logger.info("Determining election result from tally of %d total vote(s).", total_votes)

    if total_votes == 0:
        logger.error(
            "Cannot determine a result — no valid votes were cast in this election."
        )
        return {
            "status": "no_votes",
            "winner": None,
            "tally": tally,
            "margin": None,
            "margin_pct": None,
        }

    sorted_candidates = sorted(tally.items(), key=lambda x: x[1], reverse=True)
    top_candidate, top_votes = sorted_candidates[0]
    runner_up, runner_up_votes = sorted_candidates[1] if len(sorted_candidates) > 1 else (None, 0)

    # Check for a tie
    tied = [name for name, count in tally.items() if count == top_votes]
    if len(tied) > 1:
        logger.error(
            "Election result is a TIE between: %s — each received %d vote(s). "
            "A run-off or tiebreaker process is required.",
            ", ".join(sorted(tied)),
            top_votes,
        )
        return {
            "status": "tie",
            "winner": None,
            "tally": tally,
            "margin": 0,
            "margin_pct": 0.0,
        }

    margin = top_votes - runner_up_votes
    margin_pct = (margin / total_votes) * 100

    if margin_pct <= NARROW_MARGIN_THRESHOLD_PCT:
        logger.warning(
            "NARROW MARGIN — '%s' wins with %d vote(s) vs %d for '%s'. "
            "Margin: %d vote(s) (%.1f%% of total). A recount may be warranted.",
            top_candidate,
            top_votes,
            runner_up_votes,
            runner_up,
            margin,
            margin_pct,
        )
    else:
        logger.info(
            "RESULT — '%s' wins the election with %d vote(s) "
            "(margin: %d vote(s), %.1f%% of total).",
            top_candidate,
            top_votes,
            margin,
            margin_pct,
        )

    return {
        "status": "winner",
        "winner": top_candidate,
        "tally": tally,
        "margin": margin,
        "margin_pct": round(margin_pct, 2),
    }
