from nicegui import ui
from fractions import Fraction
import json

# --- Data Loading ---

with open('data_output.json') as f:
    rank720 = sorted([x[1] for x in json.load(f)], reverse=True)

with open('MATH1014MT_results_percentage.json') as f:
    m1014mt_linear = json.load(f)
with open('MATH1014MT_results_percentage_cubic.json') as f:
    m1014mt_cubic = json.load(f)
with open('MATH1014FN_results_percentage.json') as f:
    m1014fn_linear = json.load(f)
with open('MATH1014FN_results_percentage_cubic.json') as f:
    m1014fn_cubic = json.load(f)
with open('COMP2012HMT_results_percentage.json') as f:
    comp2012hmt_linear = json.load(f)
with open('COMP2012HMT_results_percentage_cubic.json') as f:
    comp2012hmt_cubic = json.load(f)


# --- Helpers ---

def count_run(lst, start, value, step=1):
    """Count consecutive occurrences of value in lst starting at start index."""
    count = 0
    i = start
    while 0 <= i < len(lst) and lst[i] == value:
        count += 1
        i += step
    return count


def format_rank(top, bottom, total):
    return f'{top}-{bottom}/{total}' if top != bottom else f'{top}/{total}'


# --- Shared UI ---

def dark_page_setup():
    ui.dark_mode(True)
    ui.query("body").classes("bg-gray-950")
    ui.query(".nicegui-content").classes("p-0 gap-0")


def page_header(title, subtitle=None):
    with ui.column().classes(
        "w-full items-center py-10 px-4 mb-8 "
        "bg-gradient-to-br from-gray-900 via-gray-900 to-cyan-950 border-b border-cyan-500/30"
    ):
        ui.label(title).classes("text-4xl font-bold text-cyan-400 tracking-tight")
        if subtitle:
            ui.label(subtitle).classes("text-gray-400 text-lg mt-1")


def nav_bar():
    with ui.row().classes("w-full max-w-2xl mx-auto gap-2 flex-wrap justify-center mb-6"):
        for label, href in [
            ("GPA Rank", "/"), ("MATH1014 MT", "/math1014mt"),
            ("MATH1014 FN", "/math1014fn"), ("COMP2012H MT", "/comp2012hmt"),
        ]:
            ui.link(label, href).classes(
                "px-4 py-2 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-500/30 "
                "hover:bg-cyan-900 hover:border-cyan-400 font-medium text-sm no-underline transition-colors"
            )


# --- GPA Rank Page ---

@ui.page('/')
async def gpa_page():
    total = len(rank720)

    def range_check(value):
        if value is None:
            return False
        return 0 <= round(value * 720) <= 3096

    def update_results(e):
        if e.value is None:
            return
        r720 = round(e.value * 720)
        result.set_text(f'{r720}/720')
        result2.set_text(f'{r720/720:.8f}')

        if r720 in rank720:
            idx = rank720.index(r720)
            run = count_run(rank720, idx, r720)
            rank_range_top = idx + 1
            rank_range_bottom = idx + run
            rank_at_u.set_text(format_rank(rank_range_top, rank_range_bottom, total))
        else:
            for i in range(total):
                if rank720[i] < r720:
                    rank_range_top = i + 1
                    rank_range_bottom = i
                    break
            else:
                rank_range_top = total
                rank_range_bottom = total - 1
            rank_at_u.set_text(f'Between {rank_range_bottom} and {rank_range_top} / {total}')

        if rank_range_bottom == total:
            rank_after_u.set_text('You are truly the worst!')
        else:
            val = rank720[rank_range_bottom]
            run = count_run(rank720, rank_range_bottom, val)
            rank_after_u.set_text(
                f'{val/720:.6f} @ {format_rank(rank_range_bottom + 1, rank_range_bottom + run, total)}')

        if rank_range_top == 1:
            rank_before_u.set_text('You are truly the best!')
        else:
            val = rank720[rank_range_top - 2]
            run = count_run(rank720, rank_range_top - 2, val, step=-1)
            rank_before_u.set_text(
                f'{val/720:.6f} @ {format_rank(rank_range_top - run, rank_range_top - 1, total)}')

        results_card.set_visibility(True)

    def is_filled(value):
        if value is not None:
            return True
        for elem in (result, result2, rank_before_u, rank_at_u, rank_after_u):
            elem.set_text("")
        results_card.set_visibility(False)
        return False

    dark_page_setup()
    page_header("Project Ordinal", "SENG Y1 GPA Rank Lookup")
    nav_bar()

    with ui.column().classes("w-full max-w-2xl mx-auto px-4"):
        with ui.card().classes("w-full p-8 rounded-2xl bg-gray-900 border border-gray-800"):
            ui.label("Enter your GPA").classes("text-lg font-semibold text-cyan-400 mb-2")
            ui.label("Fall 2022 cohort \u2022 852 students").classes("text-sm text-gray-500 mb-4")
            ui.number(label='GPA', placeholder='e.g. 3.500',
                      on_change=update_results,
                      validation={'Empty input': is_filled, 'Out of range': range_check},
                      ).classes("w-full text-lg")

        results_card = ui.card().classes("w-full p-8 rounded-2xl mt-4 bg-gray-900 border border-gray-800")
        results_card.set_visibility(False)
        with results_card:
            ui.label("Results").classes("text-lg font-semibold text-cyan-400 mb-4")

            with ui.grid(columns=2).classes("w-full gap-4"):
                with ui.column().classes("bg-cyan-950/50 rounded-xl p-4 border border-cyan-500/20"):
                    ui.label("GPA Fraction").classes("text-xs font-medium text-cyan-500 uppercase tracking-wide")
                    result = ui.label().classes("text-2xl font-bold text-cyan-300")
                with ui.column().classes("bg-cyan-950/50 rounded-xl p-4 border border-cyan-500/20"):
                    ui.label("GPA Score").classes("text-xs font-medium text-cyan-500 uppercase tracking-wide")
                    result2 = ui.label().classes("text-2xl font-bold text-cyan-300")

            ui.separator().classes("my-4")

            with ui.grid(columns=3).classes("w-full gap-4"):
                with ui.column().classes("bg-emerald-950/40 rounded-xl p-4 items-center border border-emerald-500/20"):
                    ui.label("Rank Above").classes("text-xs font-medium text-emerald-400 uppercase tracking-wide")
                    rank_before_u = ui.label().classes("text-sm font-semibold text-emerald-300 text-center")
                with ui.column().classes("bg-cyan-950/60 rounded-xl p-4 items-center border border-cyan-400/40"):
                    ui.label("Your Rank").classes("text-xs font-medium text-cyan-400 uppercase tracking-wide")
                    rank_at_u = ui.label().classes("text-xl font-bold text-cyan-300 text-center")
                with ui.column().classes("bg-rose-950/40 rounded-xl p-4 items-center border border-rose-500/20"):
                    ui.label("Rank Below").classes("text-xs font-medium text-rose-400 uppercase tracking-wide")
                    rank_after_u = ui.label().classes("text-sm font-semibold text-rose-300 text-center")


# --- Exam Score Pages ---

def exam_page(title, subtitle, label, placeholder, data_linear, data_cubic, total_students, score_fn=int):
    def update_results(e):
        if e.value is None:
            return
        try:
            idx = score_fn(e.value)
            pct_disp.set_text(f'Top {data_linear[idx] * 100:.2f}%')
            stud_disp.set_text(f'{data_linear[idx] * total_students:.0f} / {total_students}')
        except Exception:
            pct_disp.set_text("-")
            stud_disp.set_text("")
        try:
            idx = score_fn(e.value)
            pct_disp_2.set_text(f'Top {data_cubic[idx] * 100:.2f}%')
            stud_disp_2.set_text(f'{data_cubic[idx] * total_students:.0f} / {total_students}')
        except Exception:
            pct_disp_2.set_text("-")
            stud_disp_2.set_text("")
        results_card.set_visibility(True)

    dark_page_setup()
    page_header("Project Ordinal", title)
    nav_bar()

    with ui.column().classes("w-full max-w-2xl mx-auto px-4"):
        with ui.card().classes("w-full p-8 rounded-2xl bg-gray-900 border border-gray-800"):
            ui.label(label).classes("text-lg font-semibold text-cyan-400 mb-2")
            ui.label(subtitle).classes("text-sm text-gray-500 mb-4")
            ui.number(label='Score', placeholder=placeholder,
                      on_change=update_results).classes("w-full text-lg")

        results_card = ui.card().classes("w-full p-8 rounded-2xl mt-4 bg-gray-900 border border-gray-800")
        results_card.set_visibility(False)
        with results_card:
            ui.label("Results").classes("text-lg font-semibold text-cyan-400 mb-4")
            with ui.grid(columns=2).classes("w-full gap-6"):
                with ui.column().classes("bg-cyan-950/50 rounded-xl p-5 border border-cyan-500/20"):
                    ui.label("Linear Interpolation").classes("text-xs font-medium text-cyan-500 uppercase tracking-wide mb-2")
                    pct_disp = ui.label().classes("text-2xl font-bold text-cyan-300")
                    stud_disp = ui.label().classes("text-sm text-cyan-600 mt-1")
                with ui.column().classes("bg-teal-950/50 rounded-xl p-5 border border-teal-500/20"):
                    ui.label("Cubic Interpolation").classes("text-xs font-medium text-teal-500 uppercase tracking-wide mb-2")
                    pct_disp_2 = ui.label().classes("text-2xl font-bold text-teal-300")
                    stud_disp_2 = ui.label().classes("text-sm text-teal-600 mt-1")


@ui.page('/math1014mt')
async def math1014mt_page():
    exam_page("MATH1014 Midterm", "1192 students", "Enter your midterm score", "0-100",
              m1014mt_linear, m1014mt_cubic, 1192)


@ui.page('/math1014fn')
async def math1014fn_page():
    exam_page("MATH1014 Final", "1192 students", "Enter your final score", "0-100",
              m1014fn_linear, m1014fn_cubic, 1192)


@ui.page('/comp2012hmt')
async def comp2012hmt_page():
    exam_page("COMP2012H Midterm", "53 students \u2022 0.25 increment", "Enter your midterm score", "e.g. 75",
              comp2012hmt_linear, comp2012hmt_cubic, 53,
              score_fn=lambda v: int(Fraction(v) * 4))


ui.run(title="Project Ordinal")
