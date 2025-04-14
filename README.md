# WinRT OCR: Take advantage of powerful existing Windows tool

[![GitHub License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://img.shields.io/github/license/hieulhaiwork/winrt-ocr-python)
![OS](https://img.shields.io/badge/OS-Win-blue.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/hieulhaiwork/winrt-ocr-python)
[![GitHub Stars](https://img.shields.io/github/stars/hieulhaiwork/winrt-ocr-python?style=social)](https://github.com/hieulhaiwork/winrt-ocr-python/stargazers)

*If you find this repo helpful, please leave me a star, thanks!!!*

## Overview

> WinRT OCR is a Python wrapper for using OCR API from Windows Runtime (WinRT) on Windows operating system.

### 1. What is Windows Runtime (WinRT) API?

Windows Runtime is an integrated software module deeply in Windows system, first introduced after Windows 8 released. It can be simply understood as set of APIs and rules to build functions in Windows apps. 

Through APIs it provides, the developers can interact with modern functions of Windows such as location detection, camera, Bluetooth, and so on. 

[See more APIs](https://learn.microsoft.com/en-us/uwp/api/)

### 2. Which version of Windows supports WinRT API ?

It's highly recommended to use Windows 10, version 1803 or later.

The older version may lead to unwanted behaviors or no longer supported syntax.

### 3. Which language does it support to OCR?

Up to this point, WinRT has supported for several languages:

|   Code       |      Language                     |
|--------------|-----------------------------------|
| ar-SA        | Arabic (Saudi Arabia)             |
| bg-BG        | Bulgarian (Bulgaria)              |
| bs-LATN-BA   | Bosnian (Latin, Bosnia and Herzegovina) |
| cs-CZ        | Czech (Czech Republic)            |
| da-DK        | Danish (Denmark)                  |
| de-DE        | German (Germany)                  |
| el-GR        | Greek (Greece)                    |
| en-GB        | English (United Kingdom)          |
| en-US        | English (US)                      |
| es-ES        | Spanish (Spain)                   |
| es-MX        | Spanish (Mexico)                  |
| fi-FI        | Finnish (Finland)                 |
| fr-CA        | French (Canada)                   |
| fr-FR        | French (France)                   |
| hr-HR        | Croatian (Croatia)                |
| hu-HU        | Hungarian (Hungary)               |
| it-IT        | Italian (Italy)                   |
| ja-JP        | Japanese (Japan)                  |
| ko-KR        | Korean (South Korea)              |
| nb-NO        | Norwegian Bokmål (Norway)         |
| nl-NL        | Dutch (Netherlands)               |
| pl-PL        | Polish (Poland)                   |
| pt-BR        | Portuguese (Brazil)               |
| pt-PT        | Portuguese (Portugal)             |
| ro-RO        | Romanian (Romania)                |
| ru-RU        | Russian (Russia)                  |
| sk-SK        | Slovak (Slovakia)                 |
| sl-SI        | Slovenian (Slovenia)              |
| sr-CYRL-RS   | Serbian (Cyrillic, Serbia)        |
| sr-LATN-RS   | Serbian (Latin, Serbia)           |
| sv-SE        | Swedish (Sweden)                  |
| tr-TR        | Turkish (Turkey)                  |
| zh-CN        | Chinese (Simplified, China)       |
| zh-HK        | Chinese (Traditional, Hong Kong SAR) |
| zh-TW        | Chinese (Traditional, Taiwan)     |


## Recent Update

- 🚀 **2025/04/12:** Release the first version.

## Quick Start

**Dependencies:**
- Python >= 3.8
- Windows 10, version 1803 or higher

```(python)
pip install winrt-ocr-python
```
**NOTICE:**

Before you continue, check your computer to ensure that your expected language has been installed for OCR.

> Open Powershell as Administrator then run this cell:
```(powershell)
# This line will list all of language it supports for OCR (or you can see in table above)
Get-WindowsCapability -Online | Where-Object { $_.Name -Like 'Language.OCR*' }

# Download your target language (such as fr-FR)
Get-WindowsCapability -Online | Where-Object { $_.Name -Like 'Language.OCR*fr-FR*' } | Add-WindowsCapability -Online
```

This will look for the OCR language package in Window Update (WU) host then download it. It may take a few time to finish.

**Check `C:/Windows/OCR` to see that your language has been installed or not yet.** If an OCR pack is supported and installed but different location, for example, `X:/Windows/OCR`, then just copy `X:/Windows/OCR` folder to `C:/Windows/OCR` folder.

**Usage:**

```(python)
import asyncio
from winrtocr import WinRTOCR

engine = WinRTOCR()
img_path = "/path/to/img_file"
output_lines = asyncio.run(engine.ocr(img_path, lang="en-US", detail_level='line'))

# (Optional) Show languages support
engine.available_languages

# Visualize the result
# NOTE: image MUST BE str, BGR or BGRA
test_img = engine.draw_ocr_result(img_path, output_lines, detail_level='line')
```

## Acknowledgement

This library is built based on [PyWinSDK](https://github.com/pywinrt/python-winsdk). Thank for their great jobs!



