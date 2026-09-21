from typing import Optional, Any, Tuple
from core.models import LearningRoadmap, LearnerProfile, PracticeTask

def generate_strong_demo_answer(task: PracticeTask) -> str:
    """
    Generate a genuinely detailed, technically comprehensive strong answer
    specifically tailored to the CURRENT practice task's skill, topic, instructions,
    expected concepts, and evaluation criteria.
    """
    skill_lower = task.skill.lower()
    topic_lower = task.topic.lower()

    if "deep learning" in skill_lower or "pytorch" in skill_lower or "tensorflow" in skill_lower or "neural" in skill_lower:
        return (
            f"Deep learning architectures are constructed from hierarchical neural network layers that learn distributed representations. "
            f"1. Underlying Principles: Information flows via forward propagation through linear transformations and non-linear activation functions (e.g. ReLU, GELU). "
            f"A loss function computes prediction error, and backpropagation calculates gradients via the chain rule to update weights using optimizers like AdamW. "
            f"2. Implementation Approach: In PyTorch, custom architectures inherit from `torch.nn.Module`. Layers are defined in `__init__`, computation graphs are executed in `forward()`, "
            f"and training loops execute `optimizer.zero_grad()`, `loss.backward()`, and `optimizer.step()`. Production serialization utilizes TorchScript or ONNX format. "
            f"3. Production Trade-offs & Considerations: Key considerations include model parameters vs inference latency, memory bandwidth, GPU VRAM constraints, and throughput. "
            f"Techniques like mixed-precision training (fp16/bf16), model quantization (int8), and dynamic batching are applied to optimize performance."
        )

    elif "vector" in skill_lower or "cosine" in skill_lower or "embedding" in skill_lower:
        return (
            f"Vector databases store high-dimensional embedding vectors produced by neural encoders that represent semantic content in vector space. "
            f"1. Underlying Principles: Similarity search relies on distance metrics like cosine similarity (measuring angular orientation) or Euclidean distance. "
            f"Cosine similarity calculates normalized dot products where higher values indicate closer semantic alignment regardless of vector magnitude. "
            f"2. Implementation Approach: Production systems utilize specialized Approximate Nearest Neighbor (ANN) index structures such as HNSW (Hierarchical Navigable Small World) "
            f"or IVF (Inverted File Index) in databases like Pinecone, ChromaDB, or FAISS. "
            f"3. Production Trade-offs: Systems balance index build time vs query throughput, recall accuracy vs VRAM memory footprint, and pre-filtering vs post-filtering strategies under high concurrency."
        )

    elif "prompt" in skill_lower or "llm" in skill_lower:
        return (
            f"Prompt engineering involves designing structured instructions, context boundaries, and constraints to guide Large Language Models toward deterministic outputs. "
            f"1. Underlying Principles: Prompts leverage the transformer's attention mechanism by establishing role instructions, task objectives, input schemas, and output format rules. "
            f"2. Implementation Techniques: Effective strategies include Few-Shot prompting (providing high-quality input-output pairs), Chain-of-Thought reasoning (instructing step-by-step logic), "
            f"and Pydantic/JSON schema enforcement for API tool calling. "
            f"3. Production Trade-offs: Prompt designers balance context window usage (token cost and latency) against output quality, mitigate hallucination risks through explicit constraint boundaries, "
            f"and implement systematic automated evaluation benchmarks (e.g. LLM-as-a-judge)."
        )

    elif "rag" in skill_lower or "retrieval" in skill_lower:
        return (
            f"Retrieval-Augmented Generation (RAG) is an architectural pattern that enhances LLM capabilities by grounding responses in external knowledge sources. "
            f"1. Underlying Principles: Raw documents are ingested, preprocessed, and divided into semantic chunks. Chunks are converted into dense vector embeddings using an embedding model and stored in a vector index. "
            f"2. Implementation Pipeline: Upon receiving a user query, a vector database retrieves top-K relevant chunks via similarity search. These retrieved context snippets are synthesized into a structured prompt containing system instructions and user query. "
            f"3. Production Trade-offs: Key considerations include chunk size and overlap tuning, re-ranking models (Cohere Rerank) to improve precision, handling retrieval latency, and evaluating answer faithfulness vs context relevance."
        )

    else:
        concepts_str = ", ".join(task.expected_concepts) if task.expected_concepts else "underlying principles and implementation mechanics"
        criteria_str = ", ".join(task.evaluation_criteria[:2]) if task.evaluation_criteria else "operational readiness and technical clarity"
        return (
            f"Comprehensive technical overview of {task.skill} ({task.topic}): "
            f"1. Underlying Principles & Core Mechanics: {task.skill} relies on foundational principles including {concepts_str}. "
            f"It organizes system components to achieve predictable, deterministic behavior. "
            f"2. Implementation Approach: Implementation involves defining modular component boundaries, integrating relevant APIs and libraries, "
            f"and establishing robust end-to-end data processing pipelines addressing {criteria_str}. "
            f"3. Production Trade-offs & Performance Considerations: Key production trade-offs include balancing execution speed, resource utilization, "
            f"maintainability, and system scalability under load."
        )

def generate_weak_demo_answer(task: PracticeTask) -> str:
    """Generate a deliberately incomplete/weak answer for the current task."""
    return f"{task.skill} is an important technology used for software applications, but I am not sure about the specific implementation steps or trade-offs."

def build_fallback_practice_task(
    roadmap: Optional[LearningRoadmap] = None,
    week_index: int = 0,
    selected_skill: Optional[str] = None
) -> PracticeTask:
    """Build a deterministic practice task tied strictly to the selected roadmap skill."""
    target_week = (roadmap.weeks[week_index] if (roadmap and roadmap.weeks and len(roadmap.weeks) > week_index) else None)
    
    if selected_skill:
        skill = selected_skill
    elif target_week and target_week.skills_targeted:
        skill = target_week.skills_targeted[0]
    elif target_week and target_week.title:
        skill = target_week.title
    else:
        skill = "Vector Databases"

    topic = target_week.topics[0] if (target_week and target_week.topics) else f"{skill} Fundamentals"
    task_id = f"TASK_W{week_index + 1}_{skill.replace(' ', '_').upper()[:10]}"

    if "vector" in skill.lower() or "cosine" in skill.lower() or "embedding" in skill.lower():
        instructions = (
            f"Explain how {skill} works in a semantic search or RAG application. "
            f"Specifically address: (1) vector representations & embeddings, (2) similarity search mechanics like cosine similarity, "
            f"and (3) nearest-neighbor indexing in vector databases."
        )
        expected_concepts = ["embeddings", "vector representation", "similarity search", "cosine similarity", "nearest-neighbor retrieval"]
        criteria = [
            "Accurately explains how embedding vectors represent semantic meaning",
            "Describes similarity search mechanics (e.g. cosine similarity vs distance metrics)",
            "Explains nearest-neighbor indexing and retrieval in vector databases"
        ]
    elif "prompt" in skill.lower() or "llm" in skill.lower():
        instructions = (
            f"Explain key principles of {skill}. "
            f"Specifically address: (1) prompt structure & constraints, (2) few-shot learning techniques, "
            f"and (3) enforcing structured JSON outputs from LLMs."
        )
        expected_concepts = ["prompt structure", "few-shot examples", "constraints", "structured output", "system prompts"]
        criteria = [
            "Explains techniques to structure prompts and system messages",
            "Describes few-shot context injection",
            "Explains methods to enforce reliable structured JSON responses"
        ]
    elif "rag" in skill.lower() or "retrieval" in skill.lower():
        instructions = (
            f"Explain the architecture of a {skill} pipeline. "
            f"Specifically address: (1) document chunking & indexing, (2) retrieval matching, "
            f"and (3) context synthesis in the final LLM prompt."
        )
        expected_concepts = ["chunking", "vector indexing", "retrieval matching", "context synthesis", "grounded answers"]
        criteria = [
            "Explains text document chunking and vector storage",
            "Describes query retrieval matching mechanics",
            "Explains context injection into LLM prompts to prevent hallucination"
        ]
    else:
        instructions = (
            f"Explain the core technical mechanics of {skill} in a production system. "
            f"Specifically address: (1) underlying principles, (2) implementation steps, "
            f"and (3) common trade-offs or performance considerations."
        )
        expected_concepts = [skill, "underlying principles", "implementation steps", "trade-offs"]
        criteria = [
            f"Demonstrates clear understanding of {skill} principles",
            "Explains practical implementation steps accurately",
            "Identifies valid technical trade-offs"
        ]

    return PracticeTask(
        task_id=task_id,
        skill=skill,
        topic=topic,
        title=f"Practice Challenge: {skill}",
        difficulty="Intermediate",
        instructions=instructions,
        expected_concepts=expected_concepts,
        evaluation_criteria=criteria
    )

def generate_practice_task(
    roadmap: Optional[LearningRoadmap] = None,
    learner_profile: Optional[LearnerProfile] = None,
    week_index: int = 0,
    selected_skill: Optional[str] = None,
    gemini_client: Optional[Any] = None
) -> PracticeTask:
    """
    Generate a text-based practice task targeting the SPECIFIC skill/topic selected from the roadmap.
    """
    return build_fallback_practice_task(roadmap, week_index, selected_skill)
