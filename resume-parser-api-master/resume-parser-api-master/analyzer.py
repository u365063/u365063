import pandas as pd
import os
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk


def analyzer(parsedResume, context, noOfMatches, threshold):
    # nltk.download('all')
    # nltk.download('averaged_perceptron_tagger')
    print('Running the model')
    print(os.getcwd())
    df = parsedResume
    # df = pd.read_csv(
        # '/Users/rashmiranjanswain/Documents/workspace/resume-parser-api/uploads/Resume Ranking Data Set.csv')
    df_cp = df.copy()


    print('After removing the columns from dataset..')
    df_cp.isnull().sum()

    df_cp['email'].fillna('NA', inplace=True)
    df_cp['Phone number'].fillna('NA', inplace=True)
    df_cp['skills'].fillna('NA', inplace=True)
    df_cp['technical skills'].fillna('NA', inplace=True)
    df_cp['tech stack'].fillna('NA', inplace=True)

    df.isnull().sum()
    df.head()

    df = pd.read_csv('/Users/rashmiranjanswain/Documents/workspace/resume-parser-api/jdPath/UpdatedResumeDataSet.csv')
    print(df)

    with open('/Users/rashmiranjanswain/Documents/workspace/resume-parser-api/jdPath/Job Description.txt', 'r', encoding ='utf-8') as f:
        file_desc_lst =  [r.replace('\n', '') for r in f.readlines()]


    job_description = ''

    for i in file_desc_lst:
        if len(job_description) == 0:
            job_description = str(i)
        else:
            job_description = job_description + ' ' + str(i)


    all_resume_text = []

    for i in df.iloc[:].values:
        s = ''
        for j in list(i):
            if len(s) == 0:
                s = str(j)
            else:
                s = s + ' , ' + str(j)
        all_resume_text.append(s)

    cos_sim_list = get_tf_idf_cosine_similarity(job_description,all_resume_text)

    zipped_resume_rating = zip(df_cp.email,df_cp.fileName ,cos_sim_list,[x for x in range(len(df))])
    sorted_resume_rating_list = sorted(zipped_resume_rating, key = lambda x: round(x[2]*100,2))
    results = pd.DataFrame(sorted_resume_rating_list, columns=['E-Mail','File Name' ,'resume_score(%)','Ranking'])
    results['resume_score(%)'] = results.get('resume_score(%)')*100+50
    results = results[results['resume_score(%)'] >= threshold]

    return results.sort_values(by=['resume_score(%)'],ascending=False).head(noOfMatches)



def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


def get_tf_idf_cosine_similarity(job_description, all_resume_text):
    # Combine job description and resume texts
    all_texts = [job_description] + all_resume_text

    # Initialize TfidfVectorizer
    vectorizer = TfidfVectorizer()

    # Fit transform all texts and convert the TF-IDF matrix to ndarray
    tfidf_matrix = vectorizer.fit_transform(all_texts).toarray()

    # Calculate cosine similarity between job description and resume texts
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

    return cosine_similarities.flatten()  # Flatten the array for easier handling
