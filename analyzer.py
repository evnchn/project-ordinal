from pprint import pprint
from fractions import Fraction
import json
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTRect, LTLine
from scipy import stats

point = 0

y_heights = []


# https://stackoverflow.com/a/70967478
for page_layout in extract_pages("major_selection_briefing_2023_dragged.pdf"):
    for element in page_layout:
        if element.bbox[2] - element.bbox[0] < 6 and element.bbox[3] - element.bbox[1] < 6:
            point += 1
        else:
            if isinstance(element, LTTextBoxHorizontal):
                # ignore text
                continue
            if isinstance(element, LTRect):
                # ignore rects. Idk why they exist. Coordinates are meaningless.
                # print("RECT", element.bbox)
                continue
            if element.bbox[2] - element.bbox[0] > 100:
                print("HORIZ", element.bbox)
                y_heights.append(element.bbox[1])
            else:
                print("VERT", element.bbox)

y_heights.sort()

for y_height in y_heights:
    print(f"{y_height:.15f}")

print(y_heights)

cga_heights = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]

slope, intercept, r, p, std_err = stats.linregress(cga_heights, y_heights)

print(slope, intercept, r, p, std_err)


def get_height(cga):
    return slope * cga + intercept


def get_cga(height):
    return (height-intercept)/slope


print(get_height(0))


# print(get_cga(59.4))

# print(f'{point/2} points detected in first round')

# print(element.bbox)
# print("Point detected?")
# point += 1
# print(type(element))

min_height = 871871
max_height = 000000

for page_layout in extract_pages("major_selection_briefing_2023_dragged.pdf"):
    for element in page_layout:
        if element.bbox[2] - element.bbox[0] < 6 and element.bbox[3] - element.bbox[1] < 6:
            height = ((element.bbox[3] + element.bbox[1])/2)
            min_height = min(height, min_height)
            max_height = max(height, max_height)
            cga = get_cga((element.bbox[3] + element.bbox[1])/2)
            """if cga > 4:
                #print(cga)
                pass"""
            # print(cga)
print("------BEGIN SCORE OUTPUT-------")
offset = get_cga(max_height) - 4.3

cga_scores = []

for page_layout in extract_pages("major_selection_briefing_2023_dragged.pdf"):
    for element in page_layout:
        if element.bbox[2] - element.bbox[0] < 6 and element.bbox[3] - element.bbox[1] < 6:
            height = ((element.bbox[3] + element.bbox[1])/2)
            min_height = min(height, min_height)
            max_height = max(height, max_height)
            cga = get_cga((element.bbox[3] + element.bbox[1])/2) - offset
            if cga > 4 or cga < 0.5:
                print("{:16.8f}".format(cga))
                pass
            cga_scores.append(cga)
            # print(cga)


print(max_height, min_height)

cga_scores.sort()

cga_scores_2 = cga_scores[::2]

cga_scores_3 = [(x, round(x*720), 720) for x in cga_scores_2]
# for debug and visualization purposes.
# cga_scores_3 = [(Fraction(x).limit_denominator(720), float(Fraction(x).limit_denominator(720))-x) for x in cga_scores_2]

print(cga_scores_2)
print(len(cga_scores_2))

print(cga_scores_3)
print(len(cga_scores_3))

pprint(list(zip(cga_scores_2, cga_scores_3)))

cga_scores_3

with open('data_output.json', 'w') as f:
    json.dump(cga_scores_3, f)
# for debug and visualization purposes.
"""for item in cga_scores_3:
    if item[1] > 0.00000000001:
        input(item[1])"""

# Naive method. Doesn't work very accurately
"""
def get_cga_2(height):
    return 4.3/(max_height-min_height)*(height-min_height)
print("------")
for page_layout in extract_pages("major_selection_briefing_2023_dragged.pdf"):
    for element in page_layout:
        if element.bbox[2] - element.bbox[0] < 6 and element.bbox[3] - element.bbox[1] < 6:
            height = ((element.bbox[3] + element.bbox[1])/2)
            cga = get_cga_2((element.bbox[3] + element.bbox[1])/2)
            if cga > 4 or cga < 0.5:
                print(cga)
            #print(cga)"""
