# Workshop 6 learning outcomes mapped to each project.
# Used for syllabus alignment scoring in the grading prompt.

OUTCOMES = {
    1: {  # 6.2 Decision Tree Activity
        "outcomes": [
            "Identify and articulate a relevant real-world business problem",
            "Evaluate and justify the selection of decision tree-based models (LightGBM, XGBoost, CatBoost, Random Forest)",
            "Describe how decision tree algorithms solve the specific business problem",
            "Explain the added value and comparative benefits of decision tree solutions",
            "Demonstrate understanding of model mechanics and implementation considerations",
        ],
        "keywords": [
            "decision tree", "lightgbm", "xgboost", "catboost", "random forest",
            "business problem", "value add", "classification", "feature", "prediction",
            "churn", "risk", "segmentation", "supervised", "overfitting",
        ],
    },
    2: {  # 6.3 Algorithm Olympics: TF Playground
        "outcomes": [
            "Collaboratively solve classification and regression problems using TensorFlow Playground",
            "Configure and optimize neural networks to achieve test loss of 0.001 or better",
            "Minimize configuration complexity: fewest features, layers, and neurons",
            "Clearly document neural network configurations with all required fields",
            "Demonstrate practical understanding of how network components affect performance",
        ],
        "keywords": [
            "tensorflow", "classification", "regression", "test loss", "neuron", "layer",
            "activation", "learning rate", "regularization", "feature", "hidden layer",
            "relu", "sigmoid", "overfitting", "configuration",
        ],
    },
    3: {  # 6.4 Teachable Machine
        "outcomes": [
            "Build image classification model with at least 5 classes using Google Teachable Machine",
            "Build audio classification model with at least 5 classes",
            "Build pose classification model with at least 5 distinct poses",
            "Demonstrate practical knowledge of transfer learning",
            "Evaluate and document model performance including accuracy and training time",
            "Conduct peer testing and incorporate feedback",
        ],
        "keywords": [
            "teachable machine", "image", "audio", "pose", "classification",
            "transfer learning", "accuracy", "training", "sample", "class",
            "model", "screenshot", "peer", "testing",
        ],
    },
    4: {  # 6.5 GPT Hackathon
        "outcomes": [
            "Develop a Generative AI Chatbot using Retrieval-Augmented Generation (RAG)",
            "Clearly define a business problem with supporting data or statistics",
            "Integrate external data sources or real-time web search for retrieval",
            "Demonstrate product integration into existing company platforms",
            "Articulate measurable value add (efficiency, accuracy, cost, customer experience)",
            "Explain data sourcing, preprocessing, and storage methods",
            "Implement and demonstrate validation methods and guardrails",
            "Critically assess generative AI guardrails for ethics, bias, and consistency",
        ],
        "keywords": [
            "rag", "retrieval", "augmented generation", "chatbot", "llm", "gpt",
            "business problem", "data", "preprocessing", "guardrail", "validation",
            "integration", "value", "accuracy", "bias", "ethics", "web search",
        ],
    },
}

# Course-level ethical / responsible AI outcomes present across all workshops
COURSE_RAI_OUTCOMES = [
    "Apply biblical and ethical thinking to AI development",
    "Reflect on ethical and practical consequences of AI errors",
    "Address data bias considerations",
    "Demonstrate awareness of AI model explainability",
]


def keyword_precheck(text: str, project_number: int) -> dict:
    """
    Fast regex-free keyword scan against required topics.
    Returns matched/missing counts to embed as context hint in the grading prompt.
    No API call — runs before grader dispatch.
    """
    project = OUTCOMES.get(project_number, {})
    keywords = project.get("keywords", [])
    lower = text.lower()

    matched = [kw for kw in keywords if kw.lower() in lower]
    missing = [kw for kw in keywords if kw.lower() not in lower]

    coverage = round(len(matched) / len(keywords) * 100) if keywords else 0

    return {
        "coverage_pct": coverage,
        "matched": matched,
        "missing": missing,
        "total_keywords": len(keywords),
    }
