# API Mockup Flow

This folder contains the mock JSON responses for each step of the API flow. This allows us to simulate the API before writing the actual Python/FastAPI code.

## Flow Sequence

0. **Step 0 (AI Discovery)**:
   - **Endpoint**: `GET /llms.txt`
   - **Mock Data**: [llms.txt](llms.txt)
   - **Action**: The AI reads this file first. It contains the exact prompt script the AI must follow to act as a Talent Analytics Specialist and guides it on which endpoints to call.

1. **Step 1 (Baseline)**: 
   - **Endpoint**: `GET /api/v1/flow/step1?p=20&ego=t,s,r`
   - **Mock Data**: [step1.json](step1.json)
   - **Action**: The AI reads this, shows the insights to the user, and asks them to rank the top 3 traits specifically for the FIRST category.

2. **Step 1 Loop (Trait Ranking)**:
   - **Endpoint**: `GET /api/v1/flow/rank_category?s=sess_abc123&c=pk&r=1,2,3`
   - **Mock Data**: [step1_loop.json](step1_loop.json)
   - **Action**: The AI submits the first category ranking and gets the prompt to ask the user to rank the second category. This repeats 6 times. On the 6th completion, it returns the `step2.json` payload.

3. **Step 2 (Verification)**:
   - **Endpoint**: `GET /api/v1/flow/step3?session_id=sess_abc123&v=1,0,1,1...`
   - **Mock Data**: [step3.json](step3.json)
   - **Action**: The AI receives the final, precise scores for all 40 talents.

4. **Step 4 (Coaching Context)**:
   - **Endpoint**: `GET /api/v1/flow/step4?session_id=sess_abc123`
   - **Mock Data**: [step4.json](step4.json)
   - **Action**: The AI fetches the deep psychological context (weaknesses, solutions) and career recommendations to autonomously write the "Laporan Lengkap" and "Laporan Kurikulum Personalisasi".
