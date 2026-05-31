PROJECTS = {
    1: {
        "name": "6.2 Decision Tree Activity",
        "description": """
Students select a real-world business problem and discuss how decision tree-based models
(LightGBM, XGBoost, CatBoost, or Random Forest) are effective solutions.

Submission is a written write-up (no presentation) that must include:
1. Business Problem: Context, scope, significance, metrics/KPIs affected, business impact.
2. AI Solution: How specific decision tree models address the problem, model mechanics, implementation considerations.
3. Value Add: Benefits and advantages of decision tree solutions vs. other modeling approaches.
4. List of all group members.
5. Each member individually submits a short summary of the process and outcomes.

Total possible points: 70
""",
        "rubric": """
GRADING RUBRIC — 6.2 Decision Tree Activity (70 points total)

─────────────────────────────────────────────────────────────
CRITERION 1: Business Problem Definition (20 points)
─────────────────────────────────────────────────────────────
20 pts (Excellent): Comprehensive, well-defined business problem with exceptional clarity on
  context, scope, and significance. Includes specific metrics/KPIs and quantifies business impact.
  Sophisticated understanding of real-world business challenges.
18 pts (Competent): Clear, well-defined problem with good context and significance. Some metrics
  affected described. Good understanding of business challenges.
16 pts (Needs Improvement): Basic problem but definition lacks clarity or specificity. Limited
  metrics or business impact explanation.
12 pts (Inadequate/Failing): Vague, poorly defined, or inappropriate for decision trees. No
  meaningful context, significance, or business impact.

─────────────────────────────────────────────────────────────
CRITERION 2: Decision Tree Solution Analysis (20 points)
─────────────────────────────────────────────────────────────
20 pts (Excellent): Comprehensive, technically accurate analysis of specific models (LightGBM,
  XGBoost, CatBoost, Random Forest). Detailed model mechanics and implementation considerations.
18 pts (Competent): Good analysis with technical accuracy. Clear model mechanics and some
  implementation considerations.
16 pts (Needs Improvement): Basic analysis lacking technical depth or with minor inaccuracies.
  Limited mechanics or implementation explanation.
12 pts (Inadequate/Failing): Missing, severely underdeveloped, or major technical errors. No
  meaningful explanation of how models address the problem.

─────────────────────────────────────────────────────────────
CRITERION 3: Problem-Solution Alignment (20 points)
─────────────────────────────────────────────────────────────
20 pts (Excellent): Sophisticated analysis of problem features making decision trees particularly
  suitable. Specific examples and technical justification. Exceptional understanding of alignment
  between problem characteristics and decision tree capabilities.
18 pts (Competent): Good analysis of alignment with some specific examples and justification.
  Solid understanding of problem-solution fit.
16 pts (Needs Improvement): Basic alignment analysis with limited examples or justification.
  Partial understanding of why decision trees are appropriate.
12 pts (Inadequate/Failing): Missing, flawed, or fundamental misconceptions. No meaningful
  justification.

─────────────────────────────────────────────────────────────
CRITERION 4: Comparative Value Analysis (6 points)
─────────────────────────────────────────────────────────────
6 pts (Excellent): Insightful, comprehensive comparison vs. specific alternative approaches.
  Quantitative and qualitative advantages with clear trade-offs and limitations.
5 pts (Competent): Good analysis vs. some alternatives. Several advantages with some trade-offs.
4 pts (Needs Improvement): Basic analysis with limited comparison to alternatives. Few advantages,
  minimal trade-offs.
3 pts (Inadequate/Failing): Missing, underdeveloped, or inaccurate. No comparison to alternatives.

─────────────────────────────────────────────────────────────
CRITERION 5: Write-up Organization and Clarity (4 points)
─────────────────────────────────────────────────────────────
4 pts (Excellent): Exceptionally well-organized. Follows required structure perfectly. Excellent
  writing with no significant errors. Technical concepts precise for both technical and business
  audiences.
3 pts (Competent): Well-organized, follows requirements. Good writing, few minor errors. Clear
  technical explanations.
2 pts (Needs Improvement): Needs improvement, may not fully follow structure. Several errors
  occasionally impacting clarity.
1 pt (Inadequate/Failing): Poorly organized, lacks structure. Numerous errors severely impacting
  clarity.

─────────────────────────────────────────────────────────────
SCORING THRESHOLDS
─────────────────────────────────────────────────────────────
Excellent:           64+ / 70
Competent:           57+ / 70
Needs Improvement:   50+ / 70
Inadequate/Failing:   0+ / 70
"""
    },

    2: {
        "name": "6.3 Algorithm Olympics: TensorFlow Playground",
        "description": """
Teams compete to solve classification and regression problems using TensorFlow Playground.
Goal: achieve a test loss of 0.001 or better for all tasks using the MINIMUM configuration
(fewest features, layers, and total neurons).

Submission must include:
1. Detailed configurations for each task:
   - Problem type (classification or regression)
   - Features selected
   - Number of layers and neurons per layer
   - Hyperparameter settings (learning rate, activation, regularization, etc.)
   - Final test loss achieved
2. A concise team summary: strategies, rationale, challenges, and key learnings.

No formal rubric was provided. Grade holistically based on:
- Whether test loss of 0.001 was achieved for each task
- Minimization of configuration (fewer features/layers/neurons = better)
- Clarity and completeness of documentation
- Quality of team summary and reflection
""",
        "rubric": """
No formal rubric provided. Grade holistically (suggest 0–100 scale):

CONFIGURATION CORRECTNESS (40 pts):
- Did they achieve test loss ≤ 0.001 for each task? Award full credit per task completed.
- Are all required fields documented (features, layers, neurons, hyperparams, loss)?

OPTIMIZATION QUALITY (30 pts):
- Are configurations genuinely minimal? Penalize bloated configurations.
- Evidence of iterative experimentation rather than brute force.

DOCUMENTATION CLARITY (15 pts):
- Is each task clearly labeled? Are configurations unambiguous?

TEAM SUMMARY QUALITY (15 pts):
- Reflects genuine understanding of what worked and why.
- Discusses trade-offs, challenges, and learnings.
"""
    },

    3: {
        "name": "6.4 Transfer Learning: Google Teachable Machine",
        "description": """
Teams build three models using Google Teachable Machine, each with at least 5 classes:
1. Image Classification model (5+ classes)
2. Audio Classification model (5+ audio classes)
3. Pose Classification model (5+ unique poses)

Each model must be tested by a student from another team.

Submission must include:
1. Screenshots of each model showing final configuration and achieved accuracy.
2. For each model: classification categories, number of samples, final accuracy, training time.
3. A team summary: strategies, challenges, and insights.
4. List of all team members.
5. Names of the 3 students (from other groups) who tested each completed model.

No formal rubric provided. Grade holistically.
""",
        "rubric": """
No formal rubric provided. Grade holistically (suggest 0–100 scale):

MODEL COMPLETENESS (30 pts — 10 per model):
- All three models built (Image, Audio, Pose)?
- Each has at least 5 distinct classes?
- Screenshots provided showing accuracy?

ACCURACY & QUALITY (30 pts):
- Were models able to classify correctly during peer testing?
- Is accuracy reported and reasonable?

DOCUMENTATION (20 pts):
- Categories, sample counts, accuracy, and training time recorded for each model?
- Names of peer testers included?

TEAM SUMMARY (20 pts):
- Discusses strategies and rationale for class selection.
- Reflects on challenges and what was learned about transfer learning.
"""
    },

    4: {
        "name": "6.5 GPT Hackathon: Generative AI Chatbot with RAG",
        "description": """
Teams select a real-world company and build a Generative AI Chatbot using Retrieval-Augmented
Generation (RAG). The chatbot must use externally loaded data or real-time web search.

Submission is a professional slide presentation covering:
1. Real-World Generative AI Use Case (named company, real or fictitious)
2. Business Problem (with relevant data/statistics)
3. AI Solution (RAG-based, with external data retrieval details)
4. Product Integration (how it fits into existing company platforms)
5. Value Add (measurable benefits — efficiency, accuracy, cost, customer experience)
6. Data Details: source, quality, preprocessing, storage
7. Validation & Accuracy: guardrails, accuracy checks, live demo

Presentation requirements:
- Every team member must speak.
- Live chatbot demo with at least one live audience question.

Total possible points: 120
""",
        "rubric": """
GRADING RUBRIC — 6.5 GPT Hackathon (120 points total)

─────────────────────────────────────────────────────────────
CRITERION 1: Use Case & Business Problem (25 points)
─────────────────────────────────────────────────────────────
25 pts (Excellent): Exceptionally clear, compelling use case with specific named company.
  Business problem comprehensively defined with industry-specific data/statistics quantifying
  the challenge. Sophisticated understanding of business domain and AI application potential.
23 pts (Competent): Clear use case with good company context. Well-defined problem with some
  supporting data. Solid understanding of domain and AI application.
20 pts (Needs Improvement): Basic use case with minimal company context. Lacks specificity or
  compelling data. Limited understanding of domain or AI application.
16 pts (Inadequate/Failing): Vague or inappropriate use case. Poorly defined problem without
  data. Minimal understanding.

─────────────────────────────────────────────────────────────
CRITERION 2: RAG Solution & Technical Implementation (25 points)
─────────────────────────────────────────────────────────────
25 pts (Excellent): Comprehensive, technically accurate explanation of the RAG-based solution.
  Detailed technical architecture, specific LLM models, precise retrieval mechanism explanation.
  Demonstrates mastery of RAG concepts.
23 pts (Competent): Clear explanation with good technical accuracy. Adequate architecture and
  retrieval mechanism explanation. Good RAG understanding.
20 pts (Needs Improvement): Basic explanation lacking technical depth or with minor inaccuracies.
  Limited retrieval mechanism explanation. Partial RAG understanding.
16 pts (Inadequate/Failing): Missing, underdeveloped, or major technical errors. No meaningful
  retrieval explanation. Minimal RAG understanding.

─────────────────────────────────────────────────────────────
CRITERION 3: Product Integration & Value Proposition (25 points)
─────────────────────────────────────────────────────────────
25 pts (Excellent): Sophisticated, detailed integration plan with specific existing systems.
  Value proposition exceptionally well-articulated with quantifiable metrics across multiple
  benefit categories. ROI calculations or projections included.
23 pts (Competent): Clear integration plan with identified systems. Well-articulated value
  proposition with some quantifiable metrics. Basic ROI considerations.
20 pts (Needs Improvement): Basic integration plan lacking specificity. Value proposition
  present but general rather than quantified. Limited ROI.
16 pts (Inadequate/Failing): Vague, unrealistic, or missing integration. Poorly articulated
  value without metrics. No ROI.

─────────────────────────────────────────────────────────────
CRITERION 4: Data Management & Processing (25 points)
─────────────────────────────────────────────────────────────
25 pts (Excellent): Comprehensive explanation of data sources, quality, preprocessing, and
  storage with exceptional technical accuracy. Thoughtful discussion of reliability, security,
  and compliance. Sophisticated understanding of data management for RAG.
23 pts (Competent): Clear explanation of all data management aspects. Adequate reliability
  and security discussion. Solid RAG data management understanding.
20 pts (Needs Improvement): Basic explanation lacking depth in some areas. Limited reliability
  or security discussion. Partial understanding.
16 pts (Inadequate/Failing): Missing, underdeveloped, or technically inaccurate. No reliability
  or security discussion. Minimal understanding.

─────────────────────────────────────────────────────────────
CRITERION 5: Validation & Accuracy Methods (10 points)
─────────────────────────────────────────────────────────────
10 pts (Excellent): Comprehensive validation strategy with multiple specific methods for
  factual accuracy and guardrails. Detailed examples of validation in action with exceptional
  clarity on accuracy measurement and maintenance.
9 pts (Competent): Clear validation strategy with specific accuracy and guardrail methods.
  Examples with good accuracy measurement explanation.
8 pts (Needs Improvement): Basic validation approach lacking specificity or technical depth.
  Limited examples or accuracy measurement explanation.
6 pts (Inadequate/Failing): Missing, underdeveloped, or technically unsound. No meaningful
  examples or accuracy explanation.

─────────────────────────────────────────────────────────────
CRITERION 6: Presentation Quality & Professionalism (10 points)
─────────────────────────────────────────────────────────────
10 pts (Excellent): Exceptionally well-designed slides, clear organization, effective visuals,
  polished formatting. Content perfectly balanced across slides.
9 pts (Competent): Well-designed, good organization, appropriate visuals, consistent formatting.
8 pts (Needs Improvement): Inconsistent organization or formatting. Limited or poorly integrated
  visuals.
6 pts (Inadequate/Failing): Poorly designed, disorganized, unprofessional. Visuals missing or
  ineffective.

─────────────────────────────────────────────────────────────
SCORING THRESHOLDS
─────────────────────────────────────────────────────────────
Excellent:           110+ / 120
Competent:            98+ / 120
Needs Improvement:    86+ / 120
Inadequate/Failing:    0+ / 120
"""
    },
}
