# Voice System Upgrade Log

## Features Implemented
1.  **High-Fidelity TTS (ElevenLabs)**:
    - Integrated `speakWithElevenLabs` as the primary TTS engine.
    - Falls back to Kokoro -> Browser if ElevenLabs fails/is unconfigured.
    - Requires API Key in `localStorage` (`METAL_INV_11LABS`).

2.  **Robust Noise Gating (Smart Listening)**:
    - `listenFor` now accepts a `validator` function.
    - If the speech input fails validation (e.g., "Location" step receives "banana"), the synthesizer treats it as background noise and **immediately restarts listening** without annoying error prompts.
    - This creates a seamless "Always Listening" feel that only reacts to valid inputs.

3.  **Push-to-Talk (PTT) Backup**:
    - Added a "HOLD TO TALK" button in the UI.
    - **Logic**: Holding this button *bypasses* the strict validation logic.
    - **Use Case**: If the environment is extremely noisy or the regex is too strict, the user can hold PTT to force the system to accept their input.

4.  **Step-Specific Validation**:
    - **Location**: Validates phonetic mapping availability.
    - **Part/PO**: Validates format (4 digits or PO format).
    - **Quantities/Dimensions**: Validates numeric input.
    - **Confirmation**: Loops internally until "Yes", "No", or equivalent is heard.

## Usage
- **ElevenLabs**: Set raw JSON in `localStorage.setItem('METAL_INV_11LABS', JSON.stringify({ key: '...', voiceId: '...' }))`.
- **PTT**: Hold the amber button to talk. Release to stop/validate (auto-submit not strictly bound to release, but validation bypass is active while held).

## Code Changes
- `script.js`: Refactored `listenFor`, `listenOnce`, `confirmPrompt`, and all `ask*` functions. Added PTT event bindings.
- `index.html`: Added PTT button element.
