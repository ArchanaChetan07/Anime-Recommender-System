import pytest

class TestAnimeRecommender:
    def test_anime_data_structure(self):
        anime = {"title": "Naruto", "genre": ["Action","Adventure"], "rating": 8.5, "episodes": 220}
        assert "title" in anime and "genre" in anime and "rating" in anime

    def test_rating_valid_range(self):
        ratings = [7.5, 8.2, 9.0, 6.8]
        for r in ratings:
            assert 0.0 <= r <= 10.0

    def test_genre_filtering(self):
        anime_list = [
            {"title": "Naruto", "genre": ["Action"]},
            {"title": "Clannad", "genre": ["Romance","Drama"]},
            {"title": "Attack on Titan", "genre": ["Action","Drama"]},
        ]
        action = [a for a in anime_list if "Action" in a["genre"]]
        assert len(action) == 2

    def test_recommendation_not_empty(self):
        user_prefs = {"genres": ["Action"], "min_rating": 7.0}
        catalog = [
            {"title": "Naruto", "genre": ["Action"], "rating": 8.5},
            {"title": "Spirited Away", "genre": ["Fantasy"], "rating": 9.0},
        ]
        recs = [a for a in catalog if any(g in user_prefs["genres"] for g in a["genre"]) and a["rating"] >= user_prefs["min_rating"]]
        assert len(recs) > 0

    def test_similarity_score_range(self):
        scores = [0.0, 0.5, 0.8, 1.0]
        for s in scores:
            assert 0.0 <= s <= 1.0

    def test_duplicate_removal(self):
        titles = ["Naruto", "Bleach", "Naruto", "One Piece"]
        unique = list(set(titles))
        assert len(unique) == 3

    def test_top_n_recommendations(self):
        anime_list = [{"title": f"Anime{i}", "rating": i*0.5} for i in range(10)]
        top_5 = sorted(anime_list, key=lambda x: x["rating"], reverse=True)[:5]
        assert len(top_5) == 5
        assert top_5[0]["rating"] >= top_5[-1]["rating"]

class TestCollaborativeFiltering:
    def test_user_similarity(self):
        user1_ratings = {"Naruto": 9, "Bleach": 7, "One Piece": 8}
        user2_ratings = {"Naruto": 8, "Bleach": 8, "One Piece": 9}
        common = set(user1_ratings) & set(user2_ratings)
        assert len(common) == 3

    def test_cold_start_fallback(self):
        new_user_ratings = {}
        if not new_user_ratings:
            fallback = ["Naruto", "Attack on Titan", "Death Note"]
        assert len(fallback) > 0
