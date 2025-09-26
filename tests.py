import pytest

from data import ( 
    BOOK_HORROR,
    BOOK_UNKNOWN,
    GENRE_HORROR,
    GENRE_UNKNOWN,
    BOOKS_GENRE
)


class TestBooksCollector:

    def test_add_new_book_has_empty_genre(self, collector_factory):
        collector = collector_factory()
        collector.add_new_book(BOOK_HORROR)
        assert collector.books_genre[BOOK_HORROR] == ''

    @pytest.mark.parametrize('book', ['А', BOOK_HORROR, 'Б' * 40])
    def test_add_new_book_valid_books_added(self, book, collector_factory):
        collector = collector_factory()
        collector.add_new_book(book)
        assert book in collector.books_genre

    def test_add_new_book_duplicate_not_added(self, collector_factory):
        collector = collector_factory()
        collector.add_new_book(BOOK_HORROR)
        collector.add_new_book(BOOK_HORROR)
        assert list(collector.books_genre.keys()) == [BOOK_HORROR]

    @pytest.mark.parametrize('book', ['', 'А' * 41])
    def test_add_new_book_invalid_books_not_added(self, book, collector_factory):
        collector = collector_factory()
        collector.add_new_book(book)
        assert collector.books_genre == {}

    def test_get_books_genre_returns_dict(self, collector_factory):
        collector = collector_factory(books=BOOKS_GENRE)
        assert collector.get_books_genre() == BOOKS_GENRE

    def test_get_book_genre_returns_genre(self, collector_factory):
        collector = collector_factory(books={BOOK_HORROR: GENRE_HORROR})
        assert collector.get_book_genre(BOOK_HORROR) == GENRE_HORROR

    def test_set_book_genre_changes_value(self, collector_factory):
        collector = collector_factory(books={BOOK_HORROR: ''})
        collector.set_book_genre(BOOK_HORROR, GENRE_HORROR)
        assert collector.books_genre[BOOK_HORROR] == GENRE_HORROR

    def test_get_books_with_specific_genre_returns_correct_books(self, collector_factory):
        collector = collector_factory(books=BOOKS_GENRE)
        books = collector.get_books_with_specific_genre(GENRE_HORROR)
        assert all(collector.books_genre[book] == GENRE_HORROR for book in books)

    def test_get_books_with_specific_genre_unknown_returns_empty(self, collector_factory):
        collector = collector_factory(books=BOOKS_GENRE)
        assert collector.get_books_with_specific_genre(GENRE_UNKNOWN) == []

    def test_get_books_with_specific_genre_empty_collection_returns_empty(self, collector_factory):
        collector = collector_factory()
        assert collector.get_books_with_specific_genre(GENRE_HORROR) == []

    def test_get_books_for_children_returns_only_kids_books(self, collector_factory):
        collector = collector_factory(books=BOOKS_GENRE)
        books_for_children = collector.get_books_for_children()
        assert all(collector.books_genre[book] not in collector.genre_age_rating for book in books_for_children)

    @pytest.mark.parametrize('tries', [1, 2, 3])
    def test_add_book_in_favorites_no_duplicates(self, tries, collector_factory):
        collector = collector_factory(books=BOOKS_GENRE)
        for _ in range(tries):
            collector.add_book_in_favorites(BOOK_HORROR)
        assert collector.favorites == [BOOK_HORROR]

    def test_add_book_in_favorites_unknown_not_added(self, collector_factory):
        collector = collector_factory(books=BOOKS_GENRE)
        collector.add_book_in_favorites(BOOK_UNKNOWN)
        assert collector.favorites == []

    def test_delete_book_from_favorites_removes_book(self, collector_factory):
        collector = collector_factory(books=BOOKS_GENRE, favorites=[BOOK_HORROR])
        collector.delete_book_from_favorites(BOOK_HORROR)
        assert BOOK_HORROR not in collector.favorites

    def test_delete_book_from_favorites_unknown_does_nothing(self, collector_factory):
        collector = collector_factory(books=BOOKS_GENRE, favorites=[BOOK_HORROR])
        collector.delete_book_from_favorites(BOOK_UNKNOWN)
        assert collector.favorites == [BOOK_HORROR]

    def test_get_list_of_favorites_books_returns_list(self, collector_factory):
        collector = collector_factory(books=BOOKS_GENRE, favorites=[BOOK_HORROR])
        assert collector.get_list_of_favorites_books() == [BOOK_HORROR]
