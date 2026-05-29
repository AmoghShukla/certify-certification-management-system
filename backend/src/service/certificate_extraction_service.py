import base64
from pydantic import BaseModel
from pydantic_ai import Agent
from fastapi import UploadFile

class CertificateData(BaseModel):
    passing_year: int

certificate_agent = Agent(
    "google:gemini-flash-3.5",
    result_type=CertificateData,
    system_prompt=(
        "You are given an image of an academic or professional certificate. "
        "Extract only the year of passing or year of completion from it. "
        "Return just the 4-digit year as an integer. "
        "If you cannot find a year, return 0."
    )
)

class CertificateExtractionService:

    @staticmethod
    async def extract_passing_year(file: UploadFile) -> int:
        file_bytes = await file.read()
        await file.seek(0)

        b64 = base64.standard_b64encode(file_bytes).decode("utf-8")

        result = await certificate_agent.run(
            [
                {
                    "type": "image",
                    "data": b64,
                    "media_type": file.content_type or "image/jpeg",
                }
            ]
        )

        return result.data.passing_year
