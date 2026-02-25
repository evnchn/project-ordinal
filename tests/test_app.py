from nicegui import ui
from nicegui.testing import User

from serve_website import compute_percentiles, count_run, format_rank


async def test_homepage_loads(user: User) -> None:
    await user.open('/')
    await user.should_see('Project Ordinal')
    await user.should_see('Enter your GPA')


async def test_gpa_lookup_shows_results(user: User) -> None:
    await user.open('/')
    user.find(ui.number).type('3.5')
    await user.should_see('2520/720')
    await user.should_see('3.50000000')


async def test_gpa_lookup_shows_rank(user: User) -> None:
    await user.open('/')
    user.find(ui.number).type('3.5')
    await user.should_see('185-189/852')


async def test_gpa_best_rank(user: User) -> None:
    await user.open('/')
    user.find(ui.number).type('4.3')
    await user.should_see('You are truly the best!')


async def test_gpa_low_rank(user: User) -> None:
    await user.open('/')
    user.find(ui.number).type('0.5')
    await user.should_see('844-845/852')


async def test_math1014mt_page_loads(user: User) -> None:
    await user.open('/math1014mt')
    await user.should_see('Project Ordinal')
    await user.should_see('Enter your midterm score')


async def test_math1014mt_lookup(user: User) -> None:
    await user.open('/math1014mt')
    user.find(ui.number).type('75')
    await user.should_see('Top 17.16%')


async def test_math1014fn_page_loads(user: User) -> None:
    await user.open('/math1014fn')
    await user.should_see('Enter your final score')


async def test_comp2012hmt_page_loads(user: User) -> None:
    await user.open('/comp2012hmt')
    await user.should_see('COMP2012H Midterm')
    await user.should_see('0.25 increment')


async def test_navigation_links_present(user: User) -> None:
    await user.open('/')
    await user.should_see('GPA Rank')
    await user.should_see('MATH1014 MT')
    await user.should_see('MATH1014 FN')
    await user.should_see('COMP2012H MT')


def test_compute_percentiles_length():
    linear, cubic = compute_percentiles([0, 5, 10, 5], 10, 1, max_score=30)
    assert len(linear) == 31
    assert len(cubic) == 31


def test_compute_percentiles_boundaries():
    linear, _cubic = compute_percentiles([0, 5, 10, 5], 10, 1, max_score=30)
    assert linear[0] == 1.0  # score 0 -> top 100%
    assert linear[-1] == 0.0  # max score -> top 0%


def test_compute_percentiles_monotonic():
    linear, _ = compute_percentiles([0, 5, 10, 5], 10, 1, max_score=30)
    for i in range(len(linear) - 1):
        assert linear[i] >= linear[i + 1]


def test_count_run_basic():
    assert count_run([5, 5, 5, 3, 3], 0, 5) == 3
    assert count_run([5, 5, 5, 3, 3], 3, 3) == 2


def test_count_run_no_match():
    assert count_run([5, 5, 5, 3, 3], 0, 9) == 0


def test_count_run_reverse():
    assert count_run([5, 5, 5, 3, 3], 2, 5, step=-1) == 3


def test_count_run_single():
    assert count_run([1, 2, 3], 1, 2) == 1


def test_format_rank_range():
    assert format_rank(1, 3, 100) == '1-3/100'


def test_format_rank_single():
    assert format_rank(5, 5, 100) == '5/100'
