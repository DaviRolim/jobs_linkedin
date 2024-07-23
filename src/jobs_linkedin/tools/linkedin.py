from crewai_tools import BaseTool

from .client import Client as LinkedinClient


class LinkedInTool(BaseTool):
    name: str = "Retrieve LinkedIn Jobs"
    description: str = (
        "Retrieve LinkedIn Jobs given a desired position. Comma separated"
    )

    def _run(self, position: str) -> str:
        linkedin_client = LinkedinClient()
        jobs = linkedin_client.find_jobs(position)
        jobs_formatted = self._format_publications_to_text(jobs)
        linkedin_client.close()
        return jobs_formatted

    def _format_publications_to_text(self, jobs):
        result = ["\n".join([
            "Job Details",
            "-------------",
            j['name'],
            j['link'],
            j['description'],
            j["proficiency_match"]
        ]) for j in jobs]
        result = "\n\n".join(result)

        return result