'''
Reads files in a vue project folder and writes them to a markdown file
'''

import os

def read_files_in_folder(folder_path):
    markdown_file = open("./public/project.md", "w")
    # file_paths = [os.path.join(root, file) for root, dirs, files in os.walk(folder_path) for file in files]
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".vue") or file.endswith(".js") or file.endswith(".ts") or file.endswith(".css"):
                file_path = os.path.join(root, file)
                markdown_file.write(f"\n### `{file}`\n")
                markdown_file.write(f"File path: `{file_path}`\n")
                with open(file_path, "r") as f:
                    content = f.read()
                    markdown_file.write(f"```{file_path.split('.')[-1]}\n")
                    markdown_file.write(content)
                    markdown_file.write("\n```\n")
                    markdown_file.write("\n---\n")
    markdown_file.close()

def main():
    read_files_in_folder('src')
    return True


__name__ == '__main__' and main()

