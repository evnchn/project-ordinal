from nicegui import ui


3348911145

from fractions import Fraction
import json

with open('data_output.json', 'r') as f:
    cga_data = json.load(f)

rank720 = [x[1] for x in cga_data]

rank720.sort(reverse=True)
"""ui.label('Hello NiceGUI!')
ui.button('BUTTON', on_click=lambda: ui.notify('button was pressed'))"""

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

    # poe.com
    def find_indexes(numbers, target):
        # Find the index of the number just greater than the target
        for i in range(len(numbers)):
            if numbers[i] < target:
                return i, i-1
        
        # If the target is greater than all numbers in the list, return the last index
        return len(numbers)-1, len(numbers)-2

    def update_results(e):
        if not e.value:
            return
        r720 = get_closest_720frac(e.value)
        result.set_text('Estimated GPA fraction: {}/720'.format(r720))
        result2.set_text('Estimated GPA score: {:.8f}'.format(r720/720))


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
            rank_at_u.set_text('Your rank: {}/{}'.format((rank_range_top if rank_range_top == rank_range_bottom else f'{rank_range_top}-{rank_range_bottom}'), len(rank720)))
        else:
            #find_indexes(rank720, r720):
            
            i1, i2 = find_indexes(rank720, r720)
            rank_range_top = i1+1
            rank_range_bottom = i2+1

            rank_at_u.set_text(f'You rank: between {rank_range_bottom} and {rank_range_top}')


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
            rank_after_u.set_text('Rank after you: {:.6f} @ {}/{}'.format(bottom_trace/720, (rank_range_bottom+1 if rank_range_bottom+1 == rank_range_bottom+tracedown_counts else f'{rank_range_bottom+1}-{rank_range_bottom+tracedown_counts}'), len(rank720)))
        
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
            rank_before_u.set_text('Rank before you: {:.6f} @ {}/{}'.format(top_trace/720, (rank_range_top-1 if rank_range_top-1 == rank_range_top-tracedown_counts else f'{rank_range_top-tracedown_counts}-{rank_range_top-1}'), len(rank720)))




    def is_filled(input):
        if input:
            return True
        else:
            for elem in (result, result2, rank_before_u, rank_at_u, rank_after_u):
                elem.set_text("")
            return False



    ui.label("SENG Y1 GPA rank lookup").classes("text-2xl")

    ui.label("(Fall 2022 only)")

    ui.input(label='Enter your GPA', placeholder='X.XXX',
            on_change=update_results,
            validation={'Input too long': lambda value: len(value) < 20, 'Empty input': is_filled, 'Not a number': is_float, 'Out of range': range_check})


    result = ui.label()
    result2 = ui.label()

    rank_before_u = ui.label()

    rank_at_u = ui.label()

    rank_after_u = ui.label()
    
    
    
with open('MATH1014MT_results_percentage.json', 'r') as f:
    m1014mtdata = json.load(f)

with open('MATH1014MT_results_percentage_cubic.json', 'r') as f:
    m1014mtdata_2 = json.load(f)

@ui.page('/math1014mt')
async def private_page():
    
    def update_results(scorein):
        try:
            percentage_disp.set_text(f'Percentage: top {(m1014mtdata[int(scorein.value)]*100):.2f}%' )
            stud_disp.set_text(f'Rank: {(m1014mtdata[int(scorein.value)]*1192):.0f} / 1192')
        except:
            percentage_disp.set_text("Enter an integer")
            stud_disp.set_text("")
        try:
            percentage_disp_2.set_text(f'Percentage: top {(m1014mtdata_2[int(scorein.value)]*100):.2f}%' )
            stud_disp_2.set_text(f'Rank: {(m1014mtdata_2[int(scorein.value)]*1192):.0f} / 1192')
        except:
            percentage_disp_2.set_text("Enter an integer")
            stud_disp_2.set_text("")

    ui.label("MATH1014 MT score percentage lookup").classes("text-2xl")
    ui.input(label='Enter MT score', placeholder='XX',
            on_change=update_results,
            validation={})
    ui.label("Old linear interpolation")
    percentage_disp = ui.label()
    stud_disp = ui.label()

    ui.label("New cubic interpolation")
    percentage_disp_2 = ui.label()
    stud_disp_2 = ui.label()

with open('MATH1014FN_results_percentage.json', 'r') as f:
    m1014fndata = json.load(f)

with open('MATH1014FN_results_percentage_cubic.json', 'r') as f:
    m1014fndata_2 = json.load(f)

@ui.page('/math1014fn')
async def private_page():
    
    def update_results(scorein):
        try:
            percentage_disp.set_text(f'Percentage: top {(m1014fndata[int(scorein.value)]*100):.2f}%' )
            stud_disp.set_text(f'Rank: {(m1014fndata[int(scorein.value)]*1192):.0f} / 1192')
        except:
            percentage_disp.set_text("Enter an integer")
            stud_disp.set_text("")
        try:
            percentage_disp_2.set_text(f'Percentage: top {(m1014fndata_2[int(scorein.value)]*100):.2f}%' )
            stud_disp_2.set_text(f'Rank: {(m1014fndata_2[int(scorein.value)]*1192):.0f} / 1192')
        except:
            percentage_disp_2.set_text("Enter an integer")
            stud_disp_2.set_text("")

    ui.label("MATH1014 FN score percentage lookup").classes("text-2xl")
    ui.input(label='Enter FN score', placeholder='XX',
            on_change=update_results,
            validation={})
    ui.label("Old linear interpolation")
    percentage_disp = ui.label()
    stud_disp = ui.label()

    ui.label("New cubic interpolation")
    percentage_disp_2 = ui.label()
    stud_disp_2 = ui.label()


with open('COMP2012HMT_results_percentage.json', 'r') as f:
    comp2012hmtdata = json.load(f)

with open('COMP2012HMT_results_percentage_cubic.json', 'r') as f:
    comp2012hmtdata_2 = json.load(f)

@ui.page('/comp2012hmt')
async def private_page():
    
    def update_results(scorein):
        try:
            percentage_disp.set_text(f'Percentage: top {(comp2012hmtdata[int(Fraction(scorein.value)*4)]*100):.2f}%' )
            stud_disp.set_text(f'Rank: {(comp2012hmtdata[int(Fraction(scorein.value)*4)]*53):.0f} / 53')
        except:
            percentage_disp.set_text("Enter an number with 0.25 increment")
            stud_disp.set_text("")
        try:
            percentage_disp_2.set_text(f'Percentage: top {(comp2012hmtdata_2[int(Fraction(scorein.value)*4)]*100):.2f}%' )
            stud_disp_2.set_text(f'Rank: {(comp2012hmtdata_2[int(Fraction(scorein.value)*4)]*53):.0f} / 53')
        except:
            percentage_disp_2.set_text("Enter an number with 0.25 increment")
            stud_disp_2.set_text("")

    ui.label("COMP2012H MT score percentage lookup").classes("text-2xl")
    ui.input(label='Enter MT score', placeholder='XX',
            on_change=update_results,
            validation={})
    ui.label("Old linear interpolation")
    percentage_disp = ui.label()
    stud_disp = ui.label()

    ui.label("New cubic interpolation")
    percentage_disp_2 = ui.label()
    stud_disp_2 = ui.label()

ui.run(title="Project Ordinal")
