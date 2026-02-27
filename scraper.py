import requests
from bs4 import BeautifulSoup
import pandas as pd

universities = []
courses = []

uni_id = 1
course_id = 1

# read URLs
with open("urls.txt","r") as f:
    urls = f.read().splitlines()

for url in urls:
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text,"html.parser")

        title = soup.title.string.strip() if soup.title else "Unknown University"

        universities.append([
            uni_id,
            title,
            "Unknown",
            "Unknown",
            url
        ])

        # collect course-like text (headings or list items)
        items = soup.find_all(["li","h2","h3"])

        count = 0
        for i in items:
            text = i.get_text(strip=True)

            if len(text) > 10 and count < 5:
                courses.append([
                    course_id,
                    uni_id,
                    text,
                    "Unknown",
                    "Unknown",
                    "N/A",
                    "N/A",
                    "N/A"
                ])
                course_id += 1
                count += 1

        uni_id += 1

    except Exception as e:
        print("Error scraping:", url, e)


df_uni = pd.DataFrame(universities,columns=[
    "university_id","university_name","country","city","website"
])

df_courses = pd.DataFrame(courses,columns=[
    "course_id","university_id","course_name","level",
    "discipline","duration","fees","eligibility"
])

df_uni.fillna("N/A", inplace=True)
df_courses.fillna("N/A", inplace=True)

with pd.ExcelWriter("output.xlsx") as writer:
    df_uni.to_excel(writer,sheet_name="Universities",index=False)
    df_courses.to_excel(writer,sheet_name="Courses",index=False)

print("Done. Excel file created.")