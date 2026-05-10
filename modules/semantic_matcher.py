from sentence_transformers import (
    SentenceTransformer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)


# =====================================================
# LOAD MODEL
# =====================================================

model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)


# =====================================================
# SEMANTIC MATCHER
# =====================================================

def semantic_job_match(df, resume_text):

    # --------------------------------
    # JOB TEXT
    # --------------------------------

    job_texts = (

        df['clean_title'].astype(str)

        + " "

        + df['skills'].astype(str)

        + " "

        + df['description'].astype(str)

    ).tolist()

    # --------------------------------
    # EMBEDDINGS
    # --------------------------------

    job_embeddings = model.encode(
        job_texts
    )

    resume_embedding = model.encode(
        [resume_text]
    )

    # --------------------------------
    # SIMILARITY
    # --------------------------------

    similarity_scores = cosine_similarity(

        resume_embedding,

        job_embeddings

    )[0]

    return similarity_scores