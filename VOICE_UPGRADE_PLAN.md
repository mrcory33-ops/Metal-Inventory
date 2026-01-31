# Voice System Upgrade Plan

## Objective
Enhance the hands-free voice experience by implementing high-quality ElevenLabs TTS and robust "Noise Gating" to prevent background noise from interrupting the workflow. Push-to-Talk (PTT) will be added as a fallback method.

## 1. High-Quality TTS (ElevenLabs Integration)
We will introduce a new TTS adapter `speakWithElevenLabs` that takes priority over Kokoro and Browser TTS.

### Implementation Strategy
- **Client-Side API Call**: Direct calls to ElevenLabs API to keep the architecture "standalone" (no backend required).
- **Latency Optimization**: Use `streaming` endpoint or `ulaw` format if supported to minimize lag.
- **Caching**: Cache common prompts ("Location?", "Part?", "Correct?") in a simple audio cache to eliminate API latency for repeated phrases.
- **Failover**: Automatically fall back to Browser TTS if API fails or quota is exceeded.

### Configuration
We will add a settings modal or variable to input the ElevenLabs API Key and Voice ID.

## 2. "Smart Noise Gating" (Keyword Validation)
The current system accepts *any* input. We will change this to **reject and ignore** input that doesn't match the expected format for the current step.

### Logic Flow
1. **Listen**: Browser hears "clank clank [noise] uh..." -> Result: "uh"
2. **Validate**: Current Step = `LOCATION`. Expectation: `/[A-Z][0-9]+/`.
   - "uh" matches? **NO**.
3. **Action**:
   - **Old Behavior**: Returned "uh" -> App said "Retry" -> Flow interrupted.
   - **New Behavior**: Auto-discard "uh". **Immediately restart listening**. Protocol remains active. User hears nothing.
4. **Valid Input**: User says "Charlie Two". Result: "C2".
   - Matches? **YES**.
   - **Action**: Return result -> App proceeds.

### Implementation
- Modify `Speech.listenOnce` to accept a `validationRegex` or `validator` function.
- If result fails validation, recursively call `listen` again (up to N times) before giving up.

## 3. Push-to-Talk (PTT) Fallback
We will add a prominent **[HOLD TO SPEAK]** button that appears (or is always present) for environments where "Always Listening" is impossible.

- **Behavior**: User holds button -> Mic opens. User releases -> Mic closes & processes.
- **UX**: Large, touch-friendly target.

## Next Steps
1. **Refactor `script.js`**: Implement `speakWithElevenLabs`.
2. **Refactor `Speech` module**: Add noise gating loop.
3. **UI Update**: Add API Key input field and PTT button.
