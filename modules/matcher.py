from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity


def match_jobs(df, resume_text):

    # --------------------------------
    # JOB TEXT
    # --------------------------------

    df['job_text'] = (

        df['clean_title'].astype(str)

        + " "

        + df['skills'].astype(str)

        + " "

        + df['description'].astype(str)

    )

    # --------------------------------
    # TF-IDF
    # --------------------------------

    tfidf = TfidfVectorizer(
        stop_words='english'
    )

    job_vectors = tfidf.fit_transform(
        df['job_text']
    )

    # --------------------------------
    # RESUME VECTOR
    # --------------------------------

    resume_vector = tfidf.transform(
        [resume_text]
    )

    # --------------------------------
    # SIMILARITY
    # --------------------------------

    similarity = cosine_similarity(
        resume_vector,
        job_vectors
    )

    return similarity[0]