import json
import pandas as pd

with open("./examples/response_kao_soi.json") as f:
    data = f.read()
    json_data = json.loads(data)[0]

df = pd.json_normalize(json_data)
df = df.loc[(df.permanently_closed.isna()) & (df.user_ratings_total > 10)]
print(
    df[["name", "rating", "user_ratings_total", "vicinity"]].sort_values(
        ["user_ratings_total", "rating"], ascending=False
    )
)
