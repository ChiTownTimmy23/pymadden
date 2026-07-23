# pymadden

- [x] Ideally, I want to create a PyPI package that returns data for Madden 22, Madden 23, Madden 24, and Madden 25
- [x] Need to add proper logging (`logging.getLogger("pymadden")`)
- [x] Would like to use httpx and Pydantic (httpx + Pydantic v2)
- [x] Need to organize the project structure to align with best practices of a package
- [x] The endpoints for Madden 22, Madden 23, Madden 24 are the same with Madden 25 being a different endpoint (handled via `GameVersion.uses_legacy_api`)
- [x] Would like to use enums where possible (`GameVersion`, `Iteration`, `M25Iteration`)
- [x] The responses from the endpoints are different, so I'd like to be able to account for this in the package somehow (`RatingsResponse` vs `M25RatingsResponse`)
- [x] Would like to add caching, a rate limiter, and any other optimized processes (TTL cache, rate limiter, retries with backoff, concurrent pagination)
- [x] Want a function that adds on additional features that are derived from columns in the data sets (`pymadden.features.derive_features`)
- [x] Need to unpack the structs in the Madden 25 response (`M25Player.to_flat_dict()`)

## Ideas for later

- [ ] Publish to PyPI
- [ ] Optional pandas integration (`to_dataframe()` helper)
- [ ] Historical diffing between iterations (who rose/fell week over week)
- [ ] On-disk cache so repeat CLI runs are instant
