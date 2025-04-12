import traceback
from typing import Optional, Union
import os
import numpy as np

import cv2
from PIL import Image

from winsdk.windows.graphics.imaging import (
    SoftwareBitmap, BitmapPixelFormat, BitmapAlphaMode
)
from winsdk.windows.storage.streams import Buffer, DataWriter


def convert_to_np(img_input: Union[Image.Image, np.array, str]) -> Optional[np.array]:
    """
    Convert image to BGRA8 format. Only accept img_input in GRAYSCALE, BGR, RGB or BGRA.
    """
    try:
        if isinstance(img_input, str):
            if not os.path.exists(img_input):
                    print(f"Error: File not found at '{img_input}'")
                    return None
            np_img = cv2.imread(img_input, cv2.IMREAD_UNCHANGED)
            if np_img is None:
                    print(f"Error: Failed to read image file '{img_input}' with OpenCV.")
                    return None
        
        elif isinstance(img_input, Image.Image):
            img_rgba = img_input.convert('RGBA')
            np_img_rgba = np.array(img_rgba)
            np_img = cv2.cvtColor(np_img_rgba, cv2.COLOR_RGBA2BGRA)
        
        elif isinstance(img_input, np.ndarray):
            np_img = img_input
        
        else:
            print(f"Error: Unsupported input type: {type(img_input)}. Must be file path (str), PIL Image, or NumPy array.")
            return None
        
        if np_img.ndim == 2:    # Grayscale
            return cv2.cvtColor(np_img, cv2.COLOR_GRAY2BGRA)
        elif np_img.ndim == 3:
            channels = np_img.shape[2]
            if channels == 3:   # BGR or RGB
                try:
                    temp_np_img = cv2.cvtColor(np_img, cv2.COLOR_BGR2BGRA)
                    return temp_np_img
                except:
                    try:
                        temp_np_img = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGRA)
                        return temp_np_img
                    except:
                        raise ValueError("Only support img_input in GRAYSCALE, BGR, RGB, BGRA or RGBA.")
            elif channels == 4: # BGRA or RGBA
                try:
                    temp_np_image = cv2.cvtColor(np_img, cv2.COLOR_RGBA2BGRA)
                    return temp_np_image
                except:
                    # Cannot handle more situations so that if not BGRA, it may lead to unexpect result so be careful
                    return np_img

    except Exception as e:
        print(f"Error during image loading/conversion: {e}")
        traceback.print_exc()
        return None

async def _create_software_bitmap(image: Union[Image.Image, np.array, str]) -> Optional[SoftwareBitmap]:
    """
    Convert NumPy Image to SoftwareBitmap.
    """
    try:
        image_np = convert_to_np(image)
    except Exception as e:
        print("Error in converting image to BGRA format.")
        return None

    if not isinstance(image_np, np.ndarray) or image_np.ndim != 3 or image_np.shape[2] != 4:
        print(f"Error: Internal error - Input to _create_software_bitmap must be BGRA NumPy array, got shape {image_np.shape if isinstance(image_np, np.ndarray) else type(image_np)}")
        return None

    height, width, _ = image_np.shape
    pixel_data_bytes = image_np.tobytes()
    buffer_size = len(pixel_data_bytes)

    if buffer_size == 0:
        print("Error: Pixel data is empty.")
        return None

    try:
        winrt_buffer = Buffer(buffer_size)
        winrt_buffer.length = buffer_size
        writer = DataWriter()
        writer.write_bytes(pixel_data_bytes)
        filled_buffer = writer.detach_buffer()

        if filled_buffer is None or filled_buffer.length != buffer_size:
            print(f"Error: Failed to create or fill WinRT buffer. Expected size {buffer_size}, got {filled_buffer.length if filled_buffer else 'None'}")
            return None

        software_bitmap = SoftwareBitmap.create_copy_from_buffer(
            filled_buffer,
            BitmapPixelFormat.BGRA8,
            width,
            height,
            BitmapAlphaMode.PREMULTIPLIED # Usually used for BGRA. Try BitmapAlphaMode.STRAIGHT if Error.
        )
        # print(f"Successfully created SoftwareBitmap: {width}x{height}, Format: {software_bitmap.bitmap_pixel_format}, Alpha: {software_bitmap.bitmap_alpha_mode}") # For debug
        return software_bitmap

    except Exception as e:
        print(f"Error creating SoftwareBitmap: {e}")
        traceback.print_exc()
        return None