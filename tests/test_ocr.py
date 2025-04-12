import asyncio
import os
import cv2

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from winrtocr import WinRTOCR

def test_ocr():
    engine = WinRTOCR()
    output_lines = asyncio.run(engine.ocr("images/cnn_news.png", lang="en-US", detail_level='line'))
    return output_lines
        
# o_img = engine.draw_ocr_result("images/cnn_news.png", output_lines, detail_level='line')
# cv2.imwrite("images/ocr_cnn_news.png", o_img)