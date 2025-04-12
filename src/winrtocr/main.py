from typing import Optional, Tuple, Union
import os
import numpy as np
import traceback

import cv2
from PIL import Image

from winsdk.windows.media.ocr import OcrEngine
from winsdk.windows.globalization import Language

from .utils import _create_software_bitmap

class WinRTOCR():
    def __init__(self):
        self._ocr_engines = {}
    
    async def _get_ocr_engine(self, language: Language) -> Optional[OcrEngine]:
        """Initilize OcrEngine for input language."""
        lang_tag = language.language_tag
        engine = self._ocr_engines.get(lang_tag)

        if engine is None:
            print(f"Initializing OcrEngine for language: {language.display_name} ({lang_tag})...")
            try:
                engine = OcrEngine.try_create_from_language(language)
                if engine:
                    self._ocr_engines[lang_tag] = engine
                else:
                    print(f"❌ Failed: Could not create OcrEngine for {lang_tag}. Is the OCR language pack installed?")
                    self._ocr_engines[lang_tag] = None
                    return None
            except Exception as e:
                print(f"❌ Error initializing OcrEngine for {lang_tag}: {e}")
                traceback.print_exc()
                self._ocr_engines[lang_tag] = None
                return None

        if self._ocr_engines.get(lang_tag) is None:
             print(f"OcrEngine for {lang_tag} was previously determined to be unavailable.")
             return None

        return self._ocr_engines.get(lang_tag)

    async def ocr(self, img: Union[Image.Image, np.array, str], lang: str, detail_level = "line") -> Tuple[str, Tuple[float]]:
        """
        Perform ocr.
        Input:
            img (Image.Image | np.array | str): input image to OCR.
            lang (str): Target language code in BCP-47 (example: 'en-US')
            detail_leval (str): 
                - "text": Return all text in image as a line.
                - "line": Return list of tuples containing (line_text, line_bbox). (Default)
                - "word": Return list of tuples containing (line_text, line_bbox, list_of_word_results).
        """
        try:
            language = Language(lang)
        except Exception as e:
            print("Please correct input language format followed BCP-47 format. OR you can use .available_languages() to show language code.")
            return None, None
        
        engine = await self._get_ocr_engine(language)
        if engine is None:
            return None
        
        software_bitmap = await _create_software_bitmap(img)
        if software_bitmap is None:
            return None
        
        try:
            ocr_result = await engine.recognize_async(software_bitmap)
            if not ocr_result:
                print("OCR process returned no result.")
                return [] if detail_level != "text" else ""
            
            if detail_level == "text":
                return ocr_result.text if ocr_result.text else ""
            
            output_lines = []
            if ocr_result.lines:
                # print(f"Found {len(ocr_result.lines)} lines.") # For debugging
                for line in ocr_result.lines:
                    if not line.words:
                        continue
                    
                    line_text = line.text

                    # Calculate bounding box from words because ocr_result contains bbox of words not line
                    min_x, min_y = float('inf'), float('inf')
                    max_x_plus_w, max_y_plus_h = float('-inf'), float('-inf')
                    word_details = []

                    for word in line.words:
                        rect = word.bounding_rect
                        word_bbox = (int(rect.x), int(rect.y), int(rect.width), int(rect.height))

                        min_x = min(min_x, rect.x)
                        min_y = min(min_y, rect.y)
                        max_x_plus_w = max(max_x_plus_w, rect.x + rect.width)
                        max_y_plus_h = max(max_y_plus_h, rect.y + rect.height)

                        if detail_level == "word":
                            word_details.append((word.text, word_bbox))

                    if min_x != float('inf'):
                        line_bbox = (int(min_x), int(min_y), int(max_x_plus_w - min_x), int(max_y_plus_h - min_y))

                        if detail_level == "word":
                            output_lines.append((line_text, line_bbox, word_details))
                        elif detail_level == "line":
                            output_lines.append((line_text, line_bbox))

            return output_lines
        
        except Exception as e:
            print(f"Error during OCR recognition or processing: {e}")
            traceback.print_exc()
            return None

    def draw_ocr_result(self, image: Union[np.array, str], results, detail_level: str):
        """
        Draw bbox with text on image for testing.
        """
        if isinstance(image, str):
            if not os.path.exists(image):
                    print(f"Error: File not found at '{image}'")
                    return None
            image = cv2.imread(image, cv2.IMREAD_UNCHANGED)
            if image is None:
                    print(f"Error: Failed to read image file '{image}' with OpenCV.")
                    return None

        if not isinstance(image, np.ndarray):
            print("Error drawing: Input image must be a NumPy array.")
            return image
        
        output_image = image.copy()
        if output_image.ndim == 2:
            output_image = cv2.cvtColor(output_image, cv2.COLOR_GRAY2BGR)
        elif output_image.shape[2] == 4:
            output_image = cv2.cvtColor(output_image, cv2.COLOR_BGRA2BGR)

        if not results:
            print("No OCR results to draw.")
            return output_image
        
        line_color = (0, 0, 0)      # Black
        word_color = (0, 0, 0)      # Black
        thickness = 2

        for item in results:
            if detail_level == "line":
                line_text, line_bbox = item
                words_info = []
            elif detail_level == "word":
                line_text, line_bbox, words_info = item
            else: 
                continue

            x, y, w, h = line_bbox
            cv2.rectangle(output_image, (x, y), (x + w, y + h), line_color, thickness)
            cv2.putText(output_image, line_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, line_color, 1)

            if detail_level == "word" and words_info:
                for word_text, word_bbox in words_info:
                    wx, wy, ww, wh = word_bbox
                    cv2.rectangle(output_image, (wx, wy), (wx + ww, wy + wh), word_color, thickness)

        return output_image
        
    @staticmethod          
    def available_languages() -> None:
        """
        Print all languages that system supports.
        """
        languages = OcrEngine.available_recognizer_languages
        print("Support languages:")
        for language in languages:
            print(f"{language.language_tag} -> {language.display_name}")