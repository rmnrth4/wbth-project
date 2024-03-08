import pandas as pd
import nltk
import json

# download nltk corpus (first time only)
# nltk.download("all")
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


# Load the data
# f = open("file_name.json")
# # f = open("hans.json")

# data = json.load(f)

# df = []
# for entry in data:
#     texts = [
#         entry["page_title"],
#         entry["sub_title"],
#         entry["introduction"],
#         entry["summary_box"],
#         entry["content"],
#         entry["accordion"],
#     ]
#     result = " ".join(texts)
#     df.append(result)
# pandas_df = pd.DataFrame(data, columns=["text"])
# # for t in texts:
# #     if t == "":
# #         result = "".join(texts)
# #     else:
# #         result = " ".join(texts)

# # print(result)

# # Closing file
# f.close()

df = pd.read_json("file_name.json")


# Method 3: Using apply with a custom function
def merge_columns(row):
    return f"{row['page_title']} {row['sub_title']} {row['introduction']} {row['summary_box']} {row['content']} {row['accordion']}"


df["Merged_Data"] = df.apply(merge_columns, axis=1)
print(df[["Merged_Data"]])

print(df)


def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    filtered_tokens = [
        token for token in tokens if token not in stopwords.words("german")
    ]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    processed_text = " ".join(lemmatized_tokens)
    return processed_text


# pandas_df["text"] = pandas_df["text"].apply(preprocess_text)
