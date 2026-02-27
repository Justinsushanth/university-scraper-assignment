import requests
from bs4 import BeautifulSoup
import pandas as pd

# lists to store data
universities = []
courses = []

# id counters
uni_id = 1
course_id = 1

# read urls from file
with open("urls.txt", "r") as file:
    urls = file.read().splitlines()

# loop through each university url
for url in urls:
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # get university name from title
        title = soup.title.string.strip() if soup.title else "Unknown University"

        # add university data
        universities.append([
            uni_id,
            title,
            "Unknown",
            "Unknown",
            url
        ])

        # find possible course text elements
        elements = soup.find_all(["li", "h2", "h3"])

        count = 0
        for element in elements:
            text = element.get_text(strip=True)

            # filter meaningful text
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

    except Exception as error:
        print("Error scraping:", url, error)


# create dataframe for universities
df_universities = pd.DataFrame(
    universities,
    columns=[
        "university_id",
        "university_name",
        "country",
        "city",
        "website"
    ]
)

# create dataframe for courses
df_courses = pd.DataFrame(
    courses,
    columns=[
        "course_id",
        "university_id",
        "course_name",
        "level",
        "discipline",
        "duration",
        "fees",
        "eligibility"
    ]
)

# clean missing values
df_universities.fillna("N/A", inplace=True)
df_courses.fillna("N/A", inplace=True)

# save to excel
with pd.ExcelWriter("output.xlsx") as writer:
    df_universities.to_excel(writer, sheet_name="Universities", index=False)
    df_courses.to_excel(writer, sheet_name="Courses", index=False)

print("Scraping completed. Excel file generated.")
