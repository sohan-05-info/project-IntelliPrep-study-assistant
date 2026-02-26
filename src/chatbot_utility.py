import os

working_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(working_dir)

data_dir = os.path.join(parent_dir, "data_original")


def get_chapter_list(level, subject):

    subject_dir = os.path.join(data_dir, level, subject)

    if not os.path.exists(subject_dir):
        print(f"Directory not found: {subject_dir}")
        return []

    chapters_list = []

    for file in os.listdir(subject_dir):
        if file.lower().endswith(".pdf"):
            chapter_name = file[:-4]  # remove .pdf
            chapters_list.append(chapter_name)

    chapters_list.sort()

    return chapters_list


# Example usage:
# chapters = get_chapter_list("Intermediate", "DBMS")
# print(chapters)