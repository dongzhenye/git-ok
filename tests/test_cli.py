import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_PATH = REPO_ROOT / "git_ok.py"


def run(cmd, cwd=None):
    subprocess.run(
        cmd,
        cwd=cwd,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def run_cli(path, *extra_args):
    result = subprocess.run(
        [sys.executable, str(CLI_PATH), *(extra_args or []), str(path)],
        capture_output=True,
        text=True,
    )
    return result


def create_synced_repo(base_dir):
    repo_path = Path(base_dir) / "repo"
    repo_path.mkdir()
    remote_path = Path(base_dir) / "remote.git"

    run(["git", "init", "-q", "--bare", str(remote_path)])
    run(["git", "init", "-q"], cwd=repo_path)
    run(["git", "config", "user.email", "tester@example.com"], cwd=repo_path)
    run(["git", "config", "user.name", "git-ok tests"], cwd=repo_path)

    readme = repo_path / "README.md"
    readme.write_text("initial\n")
    run(["git", "add", "README.md"], cwd=repo_path)
    run(["git", "commit", "-q", "-m", "init"], cwd=repo_path)
    run(["git", "branch", "-M", "main"], cwd=repo_path)
    run(["git", "remote", "add", "origin", str(remote_path)], cwd=repo_path)
    run(["git", "push", "-q", "-u", "origin", "main"], cwd=repo_path)
    return repo_path


class GitOkCLITest(unittest.TestCase):
    def test_non_git_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_cli(tmp)
            self.assertEqual(result.returncode, 2)
            self.assertIn("Summary: not under version control", result.stdout)

    def test_clean_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = create_synced_repo(tmp)
            result = run_cli(repo)
            self.assertEqual(result.returncode, 0)
            self.assertIn("Summary: clean", result.stdout)
            self.assertIn("Local branch is in sync with remote", result.stdout)

    def test_dirty_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = create_synced_repo(tmp)
            readme = repo / "README.md"
            readme.write_text("modified\n")
            result = run_cli(repo)
            self.assertEqual(result.returncode, 1)
            self.assertIn("Summary: needs attention", result.stdout)
            self.assertIn("Working tree: changes detected", result.stdout)

    def test_unpushed_commits_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = create_synced_repo(tmp)
            extra = repo / "notes.txt"
            extra.write_text("local change\n")
            run(["git", "add", "notes.txt"], cwd=repo)
            run(["git", "commit", "-q", "-m", "local work"], cwd=repo)
            result = run_cli(repo)
            self.assertEqual(result.returncode, 1)
            self.assertIn("commits ahead of remote", result.stdout)

    def test_json_output_for_clean_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = create_synced_repo(tmp)
            result = run_cli(repo, "--json")
            self.assertEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["is_clean"])
            self.assertIn("in sync", payload["sync_status"])

    def test_important_ignored_files_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = create_synced_repo(tmp)
            gitignore = repo / ".gitignore"
            gitignore.write_text(".env\n")
            run(["git", "add", ".gitignore"], cwd=repo)
            run(["git", "commit", "-q", "-m", "ignore env"], cwd=repo)
            run(["git", "push", "-q", "origin", "main"], cwd=repo)
            env_file = repo / ".env"
            env_file.write_text("SECRET=1\n")
            result = run_cli(repo, "--json")
            self.assertEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertIn(".env", payload.get("important_ignored_files", []))

    def test_stash_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = create_synced_repo(tmp)
            readme = repo / "README.md"
            readme.write_text("stash me\n")
            run(["git", "stash", "-q"], cwd=repo)
            result = run_cli(repo)
            self.assertEqual(result.returncode, 1)
            self.assertIn("Stash: 1 stashed changes", result.stdout)


if __name__ == "__main__":
    unittest.main()
