__version__ = "0.1.0"

import platform
import asyncio

async def _check_ocr_support():
    """
    Check for suitability of current operating system and Python environment before runing OCR.
    Return True if suitable, else False with error message. 
    """

    # 1. Check operating system
    if platform.system() != "Windows":
        return False, f"Error: This API only supports for Windows system, found {platform.system()}"
    
    print(f"Operating system: {platform.system()} {platform.release()} (Version: {platform.version()})")

    # 2. Check winsdk OCR Engine import
    try:
        from winsdk.windows.media.ocr import OcrEngine
        from winsdk.windows.globalization import Language
    except ImportError:
        return False, "ERROR: Cannot import winsdk. Ensure to install it: `pip install winsdk` and runing on Windows 10/11."
    except OSError:
        return False, "OSError when import winsdk. It may be caused by lacking of basic Windows Runtime components or your Windows version does not support."
    
    # 3. Check init OCREngine
    try:
        engine = OcrEngine.try_create_from_user_profile_languages()
    except Exception as e:
        return False, e
    
    return True, ""

try:
    is_compatible, error_message = asyncio.run(_check_ocr_support())
except RuntimeError as e:
    if "Cannot run the event loop while another loop is running" in str(e):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_check_ocr_support())
    else:
        raise e

if is_compatible:
    print("✅ System passed.")
else:
    if error_message:
        raise OSError(f"❌ System failed: {error_message}")
    else:
        raise OSError(f"❌ System failed: Cannot determine the reason.")

from .main import WinRTOCR
    