# LibreFang Source List Methodology

This document outlines the methodology for managing the known_good and known_bad domain lists used by the LibreFang disinformation-detection pipeline (specifically the `source-rater` and `cib-detector` agents).

## Qualification Criteria

**Known Good**:
- Established quality journalism outlets verified by press freedom indices.
- Demonstrated adherence to editorial standards and fact-checking.

**Known Bad**:
- Documented disinformation sources verified by established OSINT registries such as IRI, EUvsDisinfo, and GLOBSEC.
- Domains repeatedly engaged in Coordinated Inauthentic Behavior (CIB) or systematic amplification of proven fake news.

## Proposing Changes

To propose the addition or removal of a domain from these lists:
1. Open a Pull Request modifying `data/source_lists/known_good.txt` or `known_bad.txt`.
2. Provide concrete evidence for your proposal (e.g., links to EUvsDisinfo database entries, independent fact-check reports, or press freedom index scores).
3. Bump the version comment header in the modified file.

## Review Cadence

These lists should be reviewed **quarterly** by maintainers to ensure they reflect the current media landscape accurately, adding emerging threats and re-evaluating existing entries.

## Known Limitations

- **Directional Bias**: The current lists have a directional bias toward pro-Kremlin coverage and Central European (Slovak/Czech) disinformation networks.
- **Coverage**: The lists do not comprehensively cover pro-Western manipulation or entirely new/ephemeral domains that emerge dynamically.
