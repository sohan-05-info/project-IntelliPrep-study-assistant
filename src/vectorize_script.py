import os
from vectorize_book import (
    vectorize_book_and_store_to_db,
    vectorize_chapters
)

# Get project root
working_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(working_dir)

data_dir = os.path.join(parent_dir, "data_original")


def vectorize_all_subjects():

    if not os.path.exists(data_dir):
        print("Data directory not found:", data_dir)
        return

    for level in os.listdir(data_dir):

        level_path = os.path.join(data_dir, level)

        if not os.path.isdir(level_path):
            continue

        for subject in os.listdir(level_path):

            subject_path = os.path.join(level_path, subject)

            if not os.path.isdir(subject_path):
                continue

            print(f"\nProcessing Level: {level} | Subject: {subject}")

            vectorize_book_and_store_to_db(
                level,
                subject,
                f"{level}_{subject}_vector_db"
            )

            vectorize_chapters(level, subject)

    print("\nAll subjects vectorized successfully!")


if __name__ == "__main__":
    vectorize_all_subjects()