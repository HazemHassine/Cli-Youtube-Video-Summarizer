#!/home/hazem/anaconda3/envs/google/bin/python3

import argparse
from youtube_transcript_api import YouTubeTranscriptApi
from main import summarize_text, youtube_url_to_id
import markdown
import os


html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="./markdown.css">
    <style>
    /* General Markdown Styles */
body {
  font-family: "Arial", sans-serif; /* Clear and modern font */
  line-height: 1.6; /* Easy to read line spacing */
  color: #333; /* Comfortable text color */
  background-color: #f9f9f9; /* Light background */
  margin: 0; /* Reset default margins */
  padding: 0;
}

/* Center and Add Margins */
.container {
  max-width: 800px; /* Keeps content at a readable width */
  margin: 2rem auto; /* Center content and add vertical spacing */
  padding: 1rem; /* Add padding inside the container */
  background: #ffffff; /* White background for content */
  border-radius: 8px; /* Rounded corners */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow for focus */
}

/* Headings */
h1,
h2,
h3,
h4,
h5,
h6 {
  color: #222; /* Slightly darker headings */
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

/* Paragraphs */
p {
  margin: 0.5rem 0; /* Space between paragraphs */
}

/* Links */
a {
  color: #0066cc;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

/* Code Blocks */
pre {
  background: #f4f4f4;
  padding: 1rem;
  border-radius: 5px;
  overflow-x: auto; /* Handles long lines of code */
}

code {
  background: #f4f4f4;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: "Courier New", Courier, monospace; /* Monospace for code */
  font-size: 0.95em;
}

/* Lists */
ul,
ol {
  margin: 1rem 0;
  padding-left: 2rem;
}

li {
  margin: 0.5rem 0;
}

/* Blockquote */
blockquote {
  margin: 1rem 0;
  padding: 1rem;
  background: #f1f1f1;
  border-left: 4px solid #ccc;
  font-style: italic;
  color: #555;
}

/* Tables */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}

th,
td {
  border: 1px solid #ddd;
  padding: 0.5rem;
  text-align: left;
}

th {
  background: #f2f2f2;
  font-weight: bold;
}
    </style>
    <title>{title}</title>
</head>
<body>
    <div class="container"><h1>{title}</h1>{here}</div>
</body>
</html>"""

yt_summaries_path = "/home/hazem/yt_summaries"

def main():
    parser = argparse.ArgumentParser(description='Example script')
    parser.add_argument('--url', type=str, help='URL to process', required=True)
    parser.add_argument('--name', type=str, help='Name to print', required=True)
    # add an argument named html which is set to false by default and is boolean if it's there
    parser.add_argument('--html', action='store_true', help='Print HTML output', default=True)

    args = parser.parse_args()

    video_id = youtube_url_to_id(args.url)
    text = "".join([i["text"] for i in YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])]).replace("\n", "")
    summary = summarize_text([text], f'Add a note on some other information you think I should know about and ressources I can go to learn more about this.')
    global html_template
    global yt_summaries_path
    print('Arguments:')
    print(f'URL: {args.url}')
    print(f'Name: {args.name}')
    # print(summary)
    if args.html:
        html_template = html_template.replace("{here}", markdown.markdown(summary))
        file_content = html_template.replace("{title}", args.name)
        
        full_html_path = os.path.join(os.getcwd(), f"{args.name}.html")
        
        with open(full_html_path, "w") as f:
            f.write(file_content)
            f.close()
            print(f"Downloaded file at: {full_html_path}")
        
        copy_path = os.path.join(yt_summaries_path, f"{args.name}.html")
        with open(copy_path, "w") as f:
            f.write(file_content)
            f.close()
            print(f"Created a copy of the file at: {copy_path}")
    else:
        with open(f"{args.name}.txt", "w") as f:
            f.write(summary)
            f.close()

if __name__ == '__main__':
    main()