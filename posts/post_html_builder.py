from pathlib import Path

path = Path(input("Path to post: "))

if not path.exists() or path.is_dir():
	print("That path doesn't exist or is a directory!")
	quit()

contents = path.read_text()
lines = contents.splitlines()

title = "Not Found"
date = "Not Found"
contents = []

for line in lines:
	line = line.strip()
	if line.removeprefix("# ") != line:
		title = line.lstrip("# ")
		continue
	if line.lstrip("> ") != line:
		date = line.lstrip("> ")
		continue
	if line:
		contents.append(line)

header = '{% extends "basePost.html" %} {% block title %}TITLE{% endblock %} {% block post_content %} <div class="header"> TITLE </div> <hr class="rounded"> <div class="numbered-paragraphs content">\n'
header = header.replace("TITLE", title)

body = ""
for paragraph in contents:
	body += "<p>" + paragraph + "</p>\n"

footer = '<div class="right-align"> DATE </div> </div> {% endblock %}'
footer = footer.replace("DATE", date)

new_html_file_text = header + body + footer
new_html_file_name = title.title().replace(" ", "_") + ".html"

result_path = Path("../templates/posts/" + new_html_file_name)
result_path.write_text(new_html_file_text)