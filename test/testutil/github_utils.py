from github import Github, InputGitAuthor

def push(author,repo,path, message, content, branch):
    contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
    ret_val = repo.update_file(contents.path, message, content, contents.sha, branch=branch,
                               author=author)  # Add, commit and push branch
    return (ret_val.get('commit'))


class GitTestRepo:
    def __init__(self,token,repo_name):
        self.token = token
        self.repo_name = repo_name
        self.repo =Github(self.token).get_repo(repo_name)


    def create_and_tag(self,author,filename,data_frame,tag_name,branch_name):
        self.repo.create_file(filename, "initial creation", data_frame.to_csv())
        fetched_file = self.repo.get_contents(filename,ref=branch_name)
        data = fetched_file.decoded_content.decode("utf-8")
        commit = push(author,self.repo,filename,"commit message",data,branch_name)
        gtag = self.repo.create_git_tag(tag=str(tag_name), message="initial load", object=commit.sha, type="commit",tagger=author)
        print('Created new file {} with tag {}'.format(filename,tag_name))
        self.repo.create_git_ref('refs/tags/{}'.format(gtag.tag), gtag.sha)





