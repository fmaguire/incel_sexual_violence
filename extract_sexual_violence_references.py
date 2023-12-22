from pathlib import Path
from tqdm import tqdm
import pandas as pd

references = {'rape': [],
              'raping': [],
              'sexual assault': [],
              'sexual assaulting': [],
              'sexually assaulting': [],
              'sexual slavery': [],
              'sex slave': [],
              'harem': []}

if __name__ == "__main__":

    with open('2022_12_11_inceldom_discussion_scrape/complete_submissions_index.txt') as fh:
        for line in tqdm(fh):
            line = line.strip().split('\t')
            url = line[0]
            submission_fp = line[1]
            user_fp = line[2]

            with open(submission_fp) as fh:
                created = next(fh).strip().replace('#created=', '')
                title = next(fh).strip().replace('#title=', '')
                reply_count = next(fh).strip().replace('#reply_count_at_start_of_scraping=', '')
                views = next(fh).strip().replace('#views_at_start_of_scraping=', '')

            try:
                submission_df = pd.read_csv(submission_fp, sep='\t', skiprows=4)
            except:
                print(f"Unreadable TSV: {submission_fp}")
            if 'comment' not in submission_df.columns:
                print(f"Malformed TSV: {submission_fp}")
                continue

            submission_df['URL'] = url
            submission_df['submission_comment_scrape'] = submission_fp
            submission_df['submission_user_scrape'] = user_fp
            submission_df['submission_creation_utc'] = created
            submission_df['submission_title'] = title
            submission_df['submission_reply_count'] = reply_count
            submission_df['submission_views'] = views
            submission_df['post_location_in_submission'] = range(len(submission_df))
            submission_df['comment'] = submission_df['comment'].fillna('')

            for name in references.keys():
                    references[name].append(submission_df[submission_df['comment'].str.lower().str.contains(name.lower())])

    for name, comments in references.items():
        comments = pd.concat(comments)
        comments.to_csv(f"sexual_violence/2022_12_11_inceldom_{name.replace(' ', '_')}_references.tsv", sep='\t')
