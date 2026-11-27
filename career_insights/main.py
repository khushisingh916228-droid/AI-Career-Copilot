def compute_readiness(resume_score, skillgap_pct, interview_avg):
    """
    Combines the three scores into one overall 'career readiness' score.
    Weights: Resume 30%, Skill Gap 40%, Interview 30%
    Any score that is not available is skipped, and the result is calculated from the rest.
    """
    valid_scores = []
    weights = []

    if resume_score is not None:
        valid_scores.append(resume_score)
        weights.append(0.3)
    if skillgap_pct is not None:
        valid_scores.append(skillgap_pct)
        weights.append(0.4)
    if interview_avg is not None:
        valid_scores.append(interview_avg * 10)  # convert the /10 score to a /100 scale
        weights.append(0.3)

    if not valid_scores:
        return None, None

    total_weight = sum(weights)
    weighted_sum = sum(s * w for s, w in zip(valid_scores, weights))
    overall = weighted_sum / total_weight

    if overall >= 80:
        label = "🟢 Job Ready"
    elif overall >= 60:
        label = "🟡 Almost There"
    elif overall >= 40:
        label = "🟠 Building Foundations"
    else:
        label = "🔴 Just Starting"

    return overall, label