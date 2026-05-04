import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.core.management.base import BaseCommand
from base.models import Category, Project


def get_github_repos(username):
    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(request, timeout=10) as response:
            return json.load(response)
    except (HTTPError, URLError, ValueError) as error:
        raise RuntimeError(f"Unable to fetch GitHub repositories: {error}")


def get_category_name(language):
    if not language:
        return "Other"
    language = language.lower()
    if language in {"python"}:
        return "Python"
    if language in {"javascript", "typescript", "php", "html", "css"}:
        return "Web Development"
    if language in {"java"}:
        return "Mobile Development"
    return "Other"


def sync_github_projects():
    repos = get_github_repos("chakhari-dotcom")
    synced_titles = []

    for repo in repos:
        title = repo.get("name", "").strip()
        if not title:
            continue

        description = repo.get("description") or ""
        technology = repo.get("language") or "Unknown"
        github_link = repo.get("html_url", "")
        category_name = get_category_name(repo.get("language"))
        category, _ = Category.objects.get_or_create(name=category_name)

        Project.objects.update_or_create(
            title=title,
            defaults={
                "description": description,
                "technology": technology,
                "category": category,
                "github_link": github_link,
            },
        )
        synced_titles.append(title)

    Project.objects.exclude(title__in=synced_titles).delete()
    return len(synced_titles)


class Command(BaseCommand):
    help = "Sync local Project records with GitHub repositories for chakhari-dotcom."

    def handle(self, *args, **options):
        try:
            count = sync_github_projects()
            self.stdout.write(self.style.SUCCESS(f"Successfully synced {count} GitHub project(s)."))
        except Exception as error:
            self.stderr.write(self.style.ERROR(f"GitHub sync failed: {error}"))
            raise
