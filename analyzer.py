"""Extract CGA scores from a PDF scatter plot and output as JSON.

Parses the major selection briefing PDF, identifies data points and axis lines,
calibrates pixel coordinates to CGA values via linear regression, and writes
the results to data_output.json.
"""

import json

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTRect, LTTextBoxHorizontal
from scipy import stats

PDF_FILE = 'major_selection_briefing_2023_dragged.pdf'
CGA_AXIS_VALUES = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]


def main():
    # Single pass: collect axis line positions and data point heights
    # Reference: https://stackoverflow.com/a/70967478
    y_heights = []
    point_heights = []

    for page_layout in extract_pages(PDF_FILE):
        for element in page_layout:
            width = element.bbox[2] - element.bbox[0]
            height = element.bbox[3] - element.bbox[1]

            if width < 6 and height < 6:
                point_heights.append((element.bbox[3] + element.bbox[1]) / 2)
            elif isinstance(element, (LTTextBoxHorizontal, LTRect)):
                continue
            elif width > 100:
                y_heights.append(element.bbox[1])

    y_heights.sort()

    # Linear regression: map pixel y-coordinates to CGA values
    slope, intercept, *_ = stats.linregress(CGA_AXIS_VALUES, y_heights)

    def pixel_to_cga(y):
        return (y - intercept) / slope

    # Calibrate offset so the maximum data point maps to CGA 4.3
    offset = pixel_to_cga(max(point_heights)) - 4.3

    # Convert pixel heights to CGA scores (points come in pairs; take every other)
    cga_scores = sorted(pixel_to_cga(h) - offset for h in point_heights)
    cga_scores = cga_scores[::2]

    # Output as (cga_float, cga_720_scale, 720) tuples
    cga_output = [(x, round(x * 720), 720) for x in cga_scores]

    with open('data_output.json', 'w') as f:
        json.dump(cga_output, f)

    print(f'Extracted {len(cga_output)} CGA scores to data_output.json')


if __name__ == '__main__':
    main()
