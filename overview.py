import streamlit as st


def render():
    st.title("Course Overview & Quick Reference")
    st.write("Select a project tab to view full requirements, background, and submission checklist.")
    st.divider()

    tabs = st.tabs([
        "6.2 Decision Trees",
        "6.3 TF Playground",
        "6.4 Teachable Machine",
        "6.5 GPT Hackathon",
    ])

    # ════════════════════════════════════════════════════════════════════════
    # 6.2 DECISION TREE ACTIVITY
    # ════════════════════════════════════════════════════════════════════════
    with tabs[0]:
        st.header("6.2 Project: Decision Tree Activity")
        st.info("**Format:** Written group write-up (no presentation) | **Points:** 70")

        st.subheader("Objective")
        st.write(
            "Select a real-world business problem and explain how a decision tree-based model "
            "(LightGBM, XGBoost, CatBoost, or Random Forest) is the right solution. "
            "Clearly outline the business problem, the AI solution, and the value added."
        )

        st.subheader("Learning Outcomes")
        st.markdown("""
- Identify and articulate a relevant real-world business problem
- Evaluate and justify the selection of decision tree-based models
- Describe how decision tree algorithms solve practical business problems
- Explain the added value and benefits of decision tree-based AI solutions
""")

        st.subheader("Background: Common Use Cases")
        st.write("Expand each industry to see an example of how decision trees are applied.")

        with st.expander("Business — Customer Segmentation & Churn Prediction"):
            st.markdown("""
**Business Problem:** Predicting customer churn to retain high-value customers.

**AI Solution:** Using Random Forest to identify patterns predicting churn based on customer interactions.

**Value Add:** Reduces customer acquisition costs by proactively retaining customers.
""")

        with st.expander("Healthcare — Medical Diagnosis"):
            st.markdown("""
**Business Problem:** Diagnosing diabetes early based on patient medical records.

**AI Solution:** Applying XGBoost to classify patients into risk categories using historical data.

**Value Add:** Enhances early diagnosis, improving patient outcomes and healthcare efficiency.
""")

        with st.expander("Finance — Credit Scoring & Risk Assessment"):
            st.markdown("""
**Business Problem:** Assessing creditworthiness to minimize lending risk.

**AI Solution:** Implementing CatBoost to predict default probability based on borrower history.

**Value Add:** Improves accuracy of risk assessments, reducing financial losses.
""")

        with st.expander("Education — Predicting Student Performance"):
            st.markdown("""
**Business Problem:** Identifying students at risk of underperforming to offer timely support.

**AI Solution:** Utilizing LightGBM to analyze academic and demographic data to predict performance.

**Value Add:** Enables early interventions, increasing student success rates.
""")

        st.subheader("Instructions")
        st.markdown("""
1. **Form groups** — stay in the same groups as the 6.1 Classroom Introductions discussion.
2. **Select a business problem** — clearly define a specific problem your group wants to address.
3. **Research the AI solution** — discuss which decision tree model fits best and why.
4. **Write the write-up** — cover all three required sections (see below).
""")

        st.subheader("What Your Write-up Must Include")
        st.markdown("""
| Section | What to Cover |
|---|---|
| **Business Problem** | Context, scope, significance, metrics/KPIs affected, quantified impact |
| **AI Solution** | Which model(s), how they work, implementation considerations |
| **Value Add** | Benefits vs. other modeling approaches, trade-offs |
| **Group Members** | List all names |
| **Individual Summary** | Each member submits their own short reflection |
""")

        st.subheader("Grading at a Glance (70 pts)")
        st.markdown("""
| Criterion | Points |
|---|---|
| Business Problem Definition | 20 |
| Decision Tree Solution Analysis | 20 |
| Problem-Solution Alignment | 20 |
| Comparative Value Analysis | 6 |
| Write-up Organization & Clarity | 4 |
| **Total** | **70** |
""")
        st.markdown("**Excellent:** 64+ &nbsp;&nbsp; **Competent:** 57+ &nbsp;&nbsp; **Needs Improvement:** 50+")

    # ════════════════════════════════════════════════════════════════════════
    # 6.3 ALGORITHM OLYMPICS
    # ════════════════════════════════════════════════════════════════════════
    with tabs[1]:
        st.header("6.3 Algorithm Olympics: TensorFlow Playground")
        st.info("**Format:** Documented configurations + team summary | **Goal:** Test loss ≤ 0.001")

        st.subheader("Objective")
        st.write(
            "Compete to solve all classification and regression tasks in TensorFlow Playground "
            "using the **minimum possible configuration** — fewest features, layers, and neurons — "
            "while still achieving a test loss of 0.001 or better."
        )

        st.subheader("Learning Outcomes")
        st.markdown("""
- Collaboratively solve problems using neural network simulations
- Configure and optimize neural networks for targeted accuracy with minimal complexity
- Document and justify neural network configurations
- Demonstrate practical understanding of how network components affect performance
""")

        st.subheader("Background: TensorFlow Playground")
        st.write("Expand each section to learn about the tool before you start.")

        with st.expander("What TensorFlow Playground Does"):
            st.markdown("""
**Visual Learning:** Real-time visual representation of how a neural network learns. Watch decision boundaries evolve as the model trains.

**Parameter Adjustment:** Easily change:
- Number of hidden layers
- Neurons per layer
- Activation functions
- Learning rate

**Immediate Feedback:** Visualizations update instantly as you change settings — showing overfitting, underfitting, and the effects of model complexity in real time.
""")

        with st.expander("How TensorFlow Playground Works"):
            st.markdown("""
1. **Dataset Selection** — Choose a 2D classification or regression dataset.
2. **Model Configuration** — Select layers, neurons, activation functions, learning rate, and regularization.
3. **Training & Visualization** — Train the network and watch the decision boundary form.
4. **Experimentation** — Adjust and compare. Small changes can have big effects.
""")

        with st.expander("What the Neural Network Does (Plain English)"):
            st.markdown("""
Think of the network as a team of tiny decision-makers working in layers:

- **Input Layer** — receives the raw data (e.g., x₁ and x₂ coordinates of a point on a graph).
- **Hidden Layers** — each neuron processes input from the previous layer and passes its "opinion" forward. Like a chain of simple yes/no questions that break the problem down step by step.
- **Output Layer** — combines everything and gives a final answer (e.g., "This point is class A").

The network *learns* by adjusting its internal settings to reduce errors. TensorFlow Playground lets you watch this happen in real time.
""")

        st.subheader("Instructions")
        st.markdown("""
1. **Form new teams** of 4–5 students.
2. **Solve every task** — both classification and regression problems in the tool.
3. **Minimize your configuration** — fewest features, layers, and neurons possible while still hitting ≤ 0.001 test loss.
4. **Document every solution** before moving to the next task.
5. **Write a team summary** when finished.
""")

        st.subheader("What to Document for Each Task")
        st.markdown("""
| Field | Example |
|---|---|
| Problem Type | Classification / Regression |
| Features Selected | X₁, X₂, X₁² |
| Layers | 2 hidden layers |
| Neurons per Layer | 4, 2 |
| Activation Function | ReLU |
| Learning Rate | 0.03 |
| Regularization | L2, 0.001 |
| Final Test Loss | 0.00087 |
""")

        st.success("**Team with the minimum configuration for each task gets to present to the class.**")

    # ════════════════════════════════════════════════════════════════════════
    # 6.4 TRANSFER LEARNING
    # ════════════════════════════════════════════════════════════════════════
    with tabs[2]:
        st.header("6.4 Transfer Learning: Google Teachable Machine")
        st.info("**Format:** Screenshots + team summary | **Models:** 3 total, 5+ classes each")

        st.subheader("Objective")
        st.write(
            "Build three custom machine learning models using Google Teachable Machine — "
            "Image, Audio, and Pose classification — each with at least 5 classes. "
            "Each completed model will be independently tested by a student from another team."
        )

        st.subheader("Learning Outcomes")
        st.markdown("""
- Build customized ML models using Google Teachable Machine
- Demonstrate practical transfer learning for image, audio, and pose classification
- Evaluate and document model performance
- Engage in collaborative peer testing and provide constructive feedback
""")

        st.subheader("Background: What Is Transfer Learning?")
        st.write(
            "Google Teachable Machine uses *transfer learning* — pre-trained neural networks "
            "(trained on massive datasets) are fine-tuned with your own small dataset. "
            "This means you can build accurate classifiers with just a few dozen examples per class."
        )
        st.write("Expand each model type below to understand how it works.")

        with st.expander("Image Classification (Vision Model)"):
            st.markdown("""
**How it works:**
- Upload or capture images for each category.
- The model uses convolutional neural networks (CNNs) to detect edges, shapes, colors, and textures.
- Transfer learning fine-tunes previously learned visual features to classify your new images.

**Example:** Recognizing fruits — apple, banana, grape, orange, pineapple.
""")

        with st.expander("Audio Classification (Speech/Audio Model)"):
            st.markdown("""
**How it works:**
- Record or upload audio clips for each category.
- The model converts audio into spectrograms (visual representations of sound frequencies).
- Transfer learning identifies unique sound patterns to differentiate between audio classes.

**Example:** Differentiating musical instruments — guitar, piano, violin, drums, flute.
""")

        with st.expander("Pose Classification (Pose Model)"):
            st.markdown("""
**How it works:**
- Capture or perform various body positions or gestures.
- The model uses computer vision to track key body points (joints: elbows, knees, wrists, etc.).
- Transfer learning learns the relative positions and movements to classify distinct poses.

**Example:** Recognizing yoga poses — tree pose, warrior pose, downward dog, cobra pose, child's pose.
""")

        st.subheader("Instructions")
        st.markdown("""
1. **Continue with your existing teams.**
2. **Build all three models** — Image, Audio, Pose — each with **5+ distinct classes**.
3. **Have each model tested** by a student from another team before submitting.
4. **Document everything** (see checklist below).
5. **Write a team summary** covering strategies, challenges, and insights.
""")

        st.subheader("Submission Checklist")
        st.markdown("""
- [ ] Screenshot of Image model — showing classes and final accuracy
- [ ] Screenshot of Audio model — showing classes and final accuracy
- [ ] Screenshot of Pose model — showing classes and final accuracy
- [ ] For each model: categories, sample count, final accuracy, training time
- [ ] Names of the 3 peer testers (one per model, from different teams)
- [ ] Team summary
- [ ] All team member names
""")

        st.success("**At the end, each group shares their 3 tasks and whether classification was successful.**")

    # ════════════════════════════════════════════════════════════════════════
    # 6.5 GPT HACKATHON
    # ════════════════════════════════════════════════════════════════════════
    with tabs[3]:
        st.header("6.5 GPT Hackathon: Generative AI Chatbot with RAG")
        st.info("**Format:** Slide presentation + live demo | **Points:** 120 | **Teams:** 5–7 students")

        st.subheader("Objective")
        st.write(
            "Select a real-world company (your own or one you work for) and build a Generative AI "
            "Chatbot using Retrieval-Augmented Generation (RAG). Your chatbot must use externally "
            "loaded data or real-time web search to deliver accurate, contextually relevant responses."
        )

        st.subheader("Learning Outcomes")
        st.markdown("""
- Develop and deploy a Generative AI Chatbot using RAG
- Define a business problem and propose an AI-driven solution
- Integrate external data sources or web retrieval to enhance chatbot accuracy
- Validate chatbot performance through live demonstration
- Present effectively, highlighting value and business integration
""")

        st.subheader("Background: What Is RAG?")
        st.write(
            "**Retrieval-Augmented Generation (RAG)** combines a powerful generative model (like GPT) "
            "with an information retrieval step. Instead of relying only on what the model was trained on, "
            "RAG *fetches* relevant external data at query time — making responses more accurate, "
            "up-to-date, and grounded in real facts."
        )

        st.subheader("Example Chatbots for Inspiration")

        with st.expander("Example 1: Delta Airlines — 'Delta Assist'"):
            st.markdown("""
**Use Case:** Chatbot handling customer queries about flight status, bookings, and travel policies.

**Business Problem:** High volumes of inquiries during delays/cancellations → long wait times, customer dissatisfaction.

**AI Solution:** Real-time web data retrieval provides passengers with immediate, accurate flight and policy info.

**Integration:** Delta's mobile app and customer service web portal.

**Value Add:** Reduced wait times, improved satisfaction, lower operational costs.

**Data:** Real-time airline APIs (structured, minimal preprocessing, temporarily stored).

**Validation:** Guardrails enforce airline policy; accuracy checked against live API data regularly.
""")

        with st.expander("Example 2: GreenLeaf Grocery — 'GreenLeaf Helper' (Fictitious)"):
            st.markdown("""
**Use Case:** Assists online grocery customers with product availability, nutrition info, and recommendations.

**Business Problem:** Cart abandonment due to uncertainty around product availability and queries.

**AI Solution:** Retrieves updated inventory and nutritional details from internal DB and external web sources.

**Integration:** GreenLeaf website and mobile app.

**Value Add:** Higher conversion rates, personalized experience, reduced service overhead.

**Data:** Internal DB + trusted external sources; moderate preprocessing; cloud storage.

**Validation:** Validated against updated inventory/nutrition DB; guardrails against incorrect nutritional advice.
""")

        with st.expander("Example 3: Netflix — 'Netflix Guide'"):
            st.markdown("""
**Use Case:** Personalized movie/show recommendations and content inquiries.

**Business Problem:** Users struggle to find relevant content → dissatisfaction and subscription churn.

**AI Solution:** Retrieves user preferences and real-time content availability from internal DB + external entertainment APIs.

**Integration:** Netflix app and website.

**Value Add:** Improved engagement, reduced churn, greater satisfaction.

**Data:** Internal user/content data + external ratings APIs; comprehensive preprocessing; strict privacy controls.

**Validation:** Guardrails ensure recommendations align with preferences; accuracy validated through user feedback and analytics.
""")

        st.subheader("Slide Deck Requirements")
        st.markdown("""
Your presentation must cover all of these slides (label them clearly):

| Slide | Content Required |
|---|---|
| Use Case | Named company + chatbot application description |
| Business Problem | Specific challenge + supporting data/statistics |
| AI Solution | RAG architecture + how retrieval works + LLM used |
| Product Integration | How chatbot fits into existing company platforms |
| Value Add | Quantifiable benefits (efficiency, accuracy, cost, CX) |
| Data Details | Source, quality, preprocessing, storage |
| Validation | Guardrails, accuracy checks, how you measure correctness |
| Live Demo | Chatbot demonstration + live audience question |
""")

        st.subheader("Presentation Rules")
        st.markdown("""
- Every team member must speak during the presentation.
- Live chatbot demo required — field at least one live question from the audience.
- Each team presents to the full class.
""")

        st.subheader("Grading at a Glance (120 pts)")
        st.markdown("""
| Criterion | Points |
|---|---|
| Use Case & Business Problem | 25 |
| RAG Solution & Technical Implementation | 25 |
| Product Integration & Value Proposition | 25 |
| Data Management & Processing | 25 |
| Validation & Accuracy Methods | 10 |
| Presentation Quality & Professionalism | 10 |
| **Total** | **120** |
""")
        st.markdown("**Excellent:** 110+ &nbsp;&nbsp; **Competent:** 98+ &nbsp;&nbsp; **Needs Improvement:** 86+")
