from nicegui import ui


3348911145

from fractions import Fraction
import json

with open('data_output.json', 'r') as f:
    cga_data = json.load(f)

rank720 = [x[1] for x in cga_data]

rank720.sort(reverse=True)


def dark_page_setup():
    ui.dark_mode(True)
    ui.query("body").classes("bg-gray-950")
    ui.query(".nicegui-content").classes("p-0 gap-0")


def page_header(title, subtitle=None):
    with ui.column().classes("w-full items-center py-10 px-4 mb-8 bg-gradient-to-br from-gray-900 via-gray-900 to-cyan-950 border-b border-cyan-500/30"):
        ui.label(title).classes("text-4xl font-bold text-cyan-400 tracking-tight")
        if subtitle:
            ui.label(subtitle).classes("text-gray-400 text-lg mt-1")


def nav_bar():
    with ui.row().classes("w-full max-w-2xl mx-auto gap-2 flex-wrap justify-center mb-6"):
        for label, href in [("GPA Rank", "/"), ("MATH1014 MT", "/math1014mt"), ("MATH1014 FN", "/math1014fn"), ("COMP2012H MT", "/comp2012hmt")]:
            ui.link(label, href).classes("px-4 py-2 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-500/30 hover:bg-cyan-900 hover:border-cyan-400 font-medium text-sm no-underline transition-colors")


@ui.page('/')
async def private_page():
    global rank720

    def range_check(value):
        if value is None:
            return False
        return not (round(value*720) > 3096 or round(value*720) < 0)

    def get_closest_720frac(value):
        times720 = value*720
        times720_low = int(times720)
        times720_high = times720_low + 1
        if abs((times720_low/720) - value) < abs((times720_high/720) - value):
            return times720_low
        else:
            return times720_high

    def find_indexes(numbers, target):
        for i in range(len(numbers)):
            if numbers[i] < target:
                return i, i-1
        return len(numbers)-1, len(numbers)-2

    def update_results(e):
        if e.value is None:
            return
        r720 = get_closest_720frac(e.value)
        result.set_text('{}/720'.format(r720))
        result2.set_text('{:.8f}'.format(r720/720))

        if r720 in rank720:
            rank = rank720.index(r720)
            tracedown_counts = 0
            for i, go_forward in list(enumerate(rank720))[rank720.index(r720):]:
                if go_forward == r720:
                    tracedown_counts += 1
                    continue
                else:
                    break
            rank_range_top = rank+1
            rank_range_bottom = rank+tracedown_counts
            rank_at_u.set_text('{}/{}'.format((rank_range_top if rank_range_top == rank_range_bottom else f'{rank_range_top}-{rank_range_bottom}'), len(rank720)))
        else:
            i1, i2 = find_indexes(rank720, r720)
            rank_range_top = i1+1
            rank_range_bottom = i2+1
            rank_at_u.set_text(f'Between {rank_range_bottom} and {rank_range_top} / {len(rank720)}')

        if rank_range_bottom == len(rank720):
            rank_after_u.set_text('You are truly the worst!')
        else:
            bottom_trace = rank720[rank_range_bottom]
            tracedown_counts = 0
            for i, go_forward in list(enumerate(rank720))[rank_range_bottom:]:
                if go_forward == bottom_trace:
                    tracedown_counts += 1
                    continue
                else:
                    break
            rank_after_u.set_text('{:.6f} @ {}/{}'.format(bottom_trace/720, (rank_range_bottom+1 if rank_range_bottom+1 == rank_range_bottom+tracedown_counts else f'{rank_range_bottom+1}-{rank_range_bottom+tracedown_counts}'), len(rank720)))

        if rank_range_top == 1:
            rank_before_u.set_text('You are truly the best!')
        else:
            top_trace = rank720[rank_range_top-2]
            tracedown_counts = 0
            for i, go_forward in list(enumerate(rank720))[rank_range_top-2::-1]:
                if go_forward == top_trace:
                    tracedown_counts += 1
                    continue
                else:
                    break
            rank_before_u.set_text('{:.6f} @ {}/{}'.format(top_trace/720, (rank_range_top-1 if rank_range_top-1 == rank_range_top-tracedown_counts else f'{rank_range_top-tracedown_counts}-{rank_range_top-1}'), len(rank720)))

        results_card.set_visibility(True)

    def is_filled(value):
        if value is not None:
            return True
        else:
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
                    validation={'Empty input': is_filled, 'Out of range': range_check}
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


with open('MATH1014MT_results_percentage.json', 'r') as f:
    m1014mtdata = json.load(f)

with open('MATH1014MT_results_percentage_cubic.json', 'r') as f:
    m1014mtdata_2 = json.load(f)


def exam_page(title, subtitle, label, placeholder, data_linear, data_cubic, total_students):
    def update_results(scorein):
        if scorein.value is None:
            return
        try:
            pct = data_linear[int(scorein.value)] * 100
            percentage_disp.set_text(f'Top {pct:.2f}%')
            stud_disp.set_text(f'{(data_linear[int(scorein.value)]*total_students):.0f} / {total_students}')
        except:
            percentage_disp.set_text("-")
            stud_disp.set_text("")
        try:
            pct2 = data_cubic[int(scorein.value)] * 100
            percentage_disp_2.set_text(f'Top {pct2:.2f}%')
            stud_disp_2.set_text(f'{(data_cubic[int(scorein.value)]*total_students):.0f} / {total_students}')
        except:
            percentage_disp_2.set_text("-")
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
                    on_change=update_results,
                    validation={}).classes("w-full text-lg")

        results_card = ui.card().classes("w-full p-8 rounded-2xl mt-4 bg-gray-900 border border-gray-800")
        results_card.set_visibility(False)
        with results_card:
            ui.label("Results").classes("text-lg font-semibold text-cyan-400 mb-4")
            with ui.grid(columns=2).classes("w-full gap-6"):
                with ui.column().classes("bg-cyan-950/50 rounded-xl p-5 border border-cyan-500/20"):
                    ui.label("Linear Interpolation").classes("text-xs font-medium text-cyan-500 uppercase tracking-wide mb-2")
                    percentage_disp = ui.label().classes("text-2xl font-bold text-cyan-300")
                    stud_disp = ui.label().classes("text-sm text-cyan-600 mt-1")
                with ui.column().classes("bg-teal-950/50 rounded-xl p-5 border border-teal-500/20"):
                    ui.label("Cubic Interpolation").classes("text-xs font-medium text-teal-500 uppercase tracking-wide mb-2")
                    percentage_disp_2 = ui.label().classes("text-2xl font-bold text-teal-300")
                    stud_disp_2 = ui.label().classes("text-sm text-teal-600 mt-1")


@ui.page('/math1014mt')
async def math1014mt_page():
    exam_page("MATH1014 Midterm", f"{1192} students", "Enter your midterm score", "0-100", m1014mtdata, m1014mtdata_2, 1192)


with open('MATH1014FN_results_percentage.json', 'r') as f:
    m1014fndata = json.load(f)

with open('MATH1014FN_results_percentage_cubic.json', 'r') as f:
    m1014fndata_2 = json.load(f)

@ui.page('/math1014fn')
async def math1014fn_page():
    exam_page("MATH1014 Final", f"{1192} students", "Enter your final score", "0-100", m1014fndata, m1014fndata_2, 1192)


with open('COMP2012HMT_results_percentage.json', 'r') as f:
    comp2012hmtdata = json.load(f)

with open('COMP2012HMT_results_percentage_cubic.json', 'r') as f:
    comp2012hmtdata_2 = json.load(f)

@ui.page('/comp2012hmt')
async def comp2012hmt_page():
    def update_results(scorein):
        if scorein.value is None:
            return
        try:
            pct = comp2012hmtdata[int(Fraction(scorein.value)*4)] * 100
            percentage_disp.set_text(f'Top {pct:.2f}%')
            stud_disp.set_text(f'{(comp2012hmtdata[int(Fraction(scorein.value)*4)]*53):.0f} / 53')
        except:
            percentage_disp.set_text("-")
            stud_disp.set_text("")
        try:
            pct2 = comp2012hmtdata_2[int(Fraction(scorein.value)*4)] * 100
            percentage_disp_2.set_text(f'Top {pct2:.2f}%')
            stud_disp_2.set_text(f'{(comp2012hmtdata_2[int(Fraction(scorein.value)*4)]*53):.0f} / 53')
        except:
            percentage_disp_2.set_text("-")
            stud_disp_2.set_text("")
        results_card.set_visibility(True)

    dark_page_setup()
    page_header("Project Ordinal", "COMP2012H Midterm")
    nav_bar()

    with ui.column().classes("w-full max-w-2xl mx-auto px-4"):
        with ui.card().classes("w-full p-8 rounded-2xl bg-gray-900 border border-gray-800"):
            ui.label("Enter your midterm score").classes("text-lg font-semibold text-cyan-400 mb-2")
            ui.label("53 students \u2022 0.25 increment").classes("text-sm text-gray-500 mb-4")
            ui.number(label='Score', placeholder='e.g. 75',
                    on_change=update_results,
                    validation={}).classes("w-full text-lg")

        results_card = ui.card().classes("w-full p-8 rounded-2xl mt-4 bg-gray-900 border border-gray-800")
        results_card.set_visibility(False)
        with results_card:
            ui.label("Results").classes("text-lg font-semibold text-cyan-400 mb-4")
            with ui.grid(columns=2).classes("w-full gap-6"):
                with ui.column().classes("bg-cyan-950/50 rounded-xl p-5 border border-cyan-500/20"):
                    ui.label("Linear Interpolation").classes("text-xs font-medium text-cyan-500 uppercase tracking-wide mb-2")
                    percentage_disp = ui.label().classes("text-2xl font-bold text-cyan-300")
                    stud_disp = ui.label().classes("text-sm text-cyan-600 mt-1")
                with ui.column().classes("bg-teal-950/50 rounded-xl p-5 border border-teal-500/20"):
                    ui.label("Cubic Interpolation").classes("text-xs font-medium text-teal-500 uppercase tracking-wide mb-2")
                    percentage_disp_2 = ui.label().classes("text-2xl font-bold text-teal-300")
                    stud_disp_2 = ui.label().classes("text-sm text-teal-600 mt-1")

ui.run(title="Project Ordinal")
