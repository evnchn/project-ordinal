from nicegui import ui


3348911145

from fractions import Fraction
import json

with open('data_output.json', 'r') as f:
    cga_data = json.load(f)

rank720 = [x[1] for x in cga_data]

rank720.sort(reverse=True)


def page_header(title, subtitle=None):
    with ui.column().classes("w-full items-center bg-gradient-to-r from-indigo-600 to-blue-500 py-10 px-4 rounded-b-2xl shadow-lg mb-8"):
        ui.label(title).classes("text-4xl font-bold text-white tracking-tight")
        if subtitle:
            ui.label(subtitle).classes("text-blue-100 text-lg mt-1")


def nav_bar():
    with ui.row().classes("w-full max-w-2xl mx-auto gap-2 flex-wrap justify-center mb-6"):
        ui.link("GPA Rank", "/").classes("px-4 py-2 rounded-full bg-indigo-50 text-indigo-700 hover:bg-indigo-100 font-medium text-sm no-underline")
        ui.link("MATH1014 MT", "/math1014mt").classes("px-4 py-2 rounded-full bg-indigo-50 text-indigo-700 hover:bg-indigo-100 font-medium text-sm no-underline")
        ui.link("MATH1014 FN", "/math1014fn").classes("px-4 py-2 rounded-full bg-indigo-50 text-indigo-700 hover:bg-indigo-100 font-medium text-sm no-underline")
        ui.link("COMP2012H MT", "/comp2012hmt").classes("px-4 py-2 rounded-full bg-indigo-50 text-indigo-700 hover:bg-indigo-100 font-medium text-sm no-underline")


@ui.page('/')
async def private_page():
    global rank720

    def is_float(str_in):
        if not str_in:
            return False
        try:
            float(str_in)
            return True
        except:
            return False

    def range_check(str_in):
        if not str_in:
            return False
        return not (round(float(str_in)*720) > 3096 or round(float(str_in)*720) < 0)

    def get_closest_720frac(str_in):
        float_in = float(str_in)
        times720 = float_in*720
        times720_low = int(times720)
        times720_high = times720_low + 1
        if abs((times720_low/720) - float_in) < abs((times720_high/720) - float_in):
            return times720_low
        else:
            return times720_high

    def find_indexes(numbers, target):
        for i in range(len(numbers)):
            if numbers[i] < target:
                return i, i-1
        return len(numbers)-1, len(numbers)-2

    def update_results(e):
        if not e.value:
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

    def is_filled(input):
        if input:
            return True
        else:
            for elem in (result, result2, rank_before_u, rank_at_u, rank_after_u):
                elem.set_text("")
            results_card.set_visibility(False)
            return False

    page_header("Project Ordinal", "SENG Y1 GPA Rank Lookup")
    nav_bar()

    with ui.column().classes("w-full max-w-2xl mx-auto px-4"):
        with ui.card().classes("w-full p-8 shadow-md rounded-2xl"):
            ui.label("Enter your GPA").classes("text-lg font-semibold text-gray-700 mb-2")
            ui.label("Fall 2022 cohort \u2022 852 students").classes("text-sm text-gray-400 mb-4")
            ui.input(label='GPA', placeholder='e.g. 3.500',
                    on_change=update_results,
                    validation={'Input too long': lambda value: len(value) < 20, 'Empty input': is_filled, 'Not a number': is_float, 'Out of range': range_check}
                    ).classes("w-full text-lg")

        results_card = ui.card().classes("w-full p-8 shadow-md rounded-2xl mt-4")
        results_card.set_visibility(False)
        with results_card:
            ui.label("Results").classes("text-lg font-semibold text-gray-700 mb-4")

            with ui.grid(columns=2).classes("w-full gap-4"):
                with ui.column().classes("bg-indigo-50 rounded-xl p-4"):
                    ui.label("GPA Fraction").classes("text-xs font-medium text-indigo-400 uppercase tracking-wide")
                    result = ui.label().classes("text-2xl font-bold text-indigo-700")
                with ui.column().classes("bg-blue-50 rounded-xl p-4"):
                    ui.label("GPA Score").classes("text-xs font-medium text-blue-400 uppercase tracking-wide")
                    result2 = ui.label().classes("text-2xl font-bold text-blue-700")

            ui.separator().classes("my-4")

            with ui.grid(columns=3).classes("w-full gap-4"):
                with ui.column().classes("bg-green-50 rounded-xl p-4 items-center"):
                    ui.label("Rank Above").classes("text-xs font-medium text-green-500 uppercase tracking-wide")
                    rank_before_u = ui.label().classes("text-sm font-semibold text-green-700 text-center")
                with ui.column().classes("bg-amber-50 rounded-xl p-4 items-center"):
                    ui.label("Your Rank").classes("text-xs font-medium text-amber-500 uppercase tracking-wide")
                    rank_at_u = ui.label().classes("text-xl font-bold text-amber-700 text-center")
                with ui.column().classes("bg-red-50 rounded-xl p-4 items-center"):
                    ui.label("Rank Below").classes("text-xs font-medium text-red-400 uppercase tracking-wide")
                    rank_after_u = ui.label().classes("text-sm font-semibold text-red-700 text-center")


with open('MATH1014MT_results_percentage.json', 'r') as f:
    m1014mtdata = json.load(f)

with open('MATH1014MT_results_percentage_cubic.json', 'r') as f:
    m1014mtdata_2 = json.load(f)


def exam_page(title, subtitle, label, placeholder, data_linear, data_cubic, total_students):
    def update_results(scorein):
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

    page_header("Project Ordinal", title)
    nav_bar()

    with ui.column().classes("w-full max-w-2xl mx-auto px-4"):
        with ui.card().classes("w-full p-8 shadow-md rounded-2xl"):
            ui.label(label).classes("text-lg font-semibold text-gray-700 mb-2")
            ui.label(subtitle).classes("text-sm text-gray-400 mb-4")
            ui.input(label='Score', placeholder=placeholder,
                    on_change=update_results,
                    validation={}).classes("w-full text-lg")

        results_card = ui.card().classes("w-full p-8 shadow-md rounded-2xl mt-4")
        results_card.set_visibility(False)
        with results_card:
            ui.label("Results").classes("text-lg font-semibold text-gray-700 mb-4")
            with ui.grid(columns=2).classes("w-full gap-6"):
                with ui.column().classes("bg-blue-50 rounded-xl p-5"):
                    ui.label("Linear Interpolation").classes("text-xs font-medium text-blue-400 uppercase tracking-wide mb-2")
                    percentage_disp = ui.label().classes("text-2xl font-bold text-blue-700")
                    stud_disp = ui.label().classes("text-sm text-blue-500 mt-1")
                with ui.column().classes("bg-indigo-50 rounded-xl p-5"):
                    ui.label("Cubic Interpolation").classes("text-xs font-medium text-indigo-400 uppercase tracking-wide mb-2")
                    percentage_disp_2 = ui.label().classes("text-2xl font-bold text-indigo-700")
                    stud_disp_2 = ui.label().classes("text-sm text-indigo-500 mt-1")


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

    page_header("Project Ordinal", "COMP2012H Midterm")
    nav_bar()

    with ui.column().classes("w-full max-w-2xl mx-auto px-4"):
        with ui.card().classes("w-full p-8 shadow-md rounded-2xl"):
            ui.label("Enter your midterm score").classes("text-lg font-semibold text-gray-700 mb-2")
            ui.label("53 students \u2022 0.25 increment").classes("text-sm text-gray-400 mb-4")
            ui.input(label='Score', placeholder='e.g. 75',
                    on_change=update_results,
                    validation={}).classes("w-full text-lg")

        results_card = ui.card().classes("w-full p-8 shadow-md rounded-2xl mt-4")
        results_card.set_visibility(False)
        with results_card:
            ui.label("Results").classes("text-lg font-semibold text-gray-700 mb-4")
            with ui.grid(columns=2).classes("w-full gap-6"):
                with ui.column().classes("bg-blue-50 rounded-xl p-5"):
                    ui.label("Linear Interpolation").classes("text-xs font-medium text-blue-400 uppercase tracking-wide mb-2")
                    percentage_disp = ui.label().classes("text-2xl font-bold text-blue-700")
                    stud_disp = ui.label().classes("text-sm text-blue-500 mt-1")
                with ui.column().classes("bg-indigo-50 rounded-xl p-5"):
                    ui.label("Cubic Interpolation").classes("text-xs font-medium text-indigo-400 uppercase tracking-wide mb-2")
                    percentage_disp_2 = ui.label().classes("text-2xl font-bold text-indigo-700")
                    stud_disp_2 = ui.label().classes("text-sm text-indigo-500 mt-1")

ui.run(title="Project Ordinal")
