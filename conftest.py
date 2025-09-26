import pytest

from main import BooksCollector

@pytest.fixture
def collector_factory():
    def _create_collector(books=None, favorites=None):
        collector = BooksCollector()
        if books:
            for name, genre in books.items():
                collector.add_new_book(name)
                if genre:
                    collector.set_book_genre(name, genre)
        if favorites:
            for name in favorites:
                collector.add_book_in_favorites(name)
        return collector
    return _create_collector
