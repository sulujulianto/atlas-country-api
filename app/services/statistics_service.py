from typing import Dict, List

from app.repositories import CapitalRepository, CountryRepository


class StatisticsService:
    def __init__(self, country_repo: CountryRepository, capital_repo: CapitalRepository):
        self.country_repo = country_repo
        self.capital_repo = capital_repo

    def total_countries(self) -> int:
        return len(self.country_repo.get_all_countries())

    def total_capitals(self) -> int:
        return len(self.capital_repo.get_all_capitals())

    def top_largest_populations(self, limit: int = 5) -> List[dict]:
        if limit <= 0:
            from app.exceptions import BadRequestError
            raise BadRequestError("limit must be positive", {"limit": limit})
        countries = self.country_repo.get_all_countries()
        ranked = sorted(countries, key=lambda c: c.population, reverse=True)[:limit]
        return [c.model_dump() for c in ranked]

    def top_smallest_populations(self, limit: int = 5) -> List[dict]:
        if limit <= 0:
            from app.exceptions import BadRequestError
            raise BadRequestError("limit must be positive", {"limit": limit})
        countries = self.country_repo.get_all_countries()
        ranked = sorted(countries, key=lambda c: c.population)[:limit]
        return [c.model_dump() for c in ranked]

    def region_distribution(self) -> Dict[str, int]:
        regions: Dict[str, int] = {}
        for c in self.country_repo.get_all_countries():
            regions[c.region] = regions.get(c.region, 0) + 1
        return regions

    def language_distribution(self) -> Dict[str, int]:
        langs: Dict[str, int] = {}
        for c in self.country_repo.get_all_countries():
            for lang in c.languages:
                langs[lang] = langs.get(lang, 0) + 1
        return langs
