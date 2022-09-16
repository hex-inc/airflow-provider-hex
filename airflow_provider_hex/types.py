from typing import TypedDict

RunResponse = TypedDict(
    "RunResponse",
    {
        "projectId": str,
        "runId": str,
        "runUrl": str,
        "runStatusUrl": str,
        "traceId": str,
    },
)

StatusResponse = TypedDict(
    "StatusResponse",
    {
        "projectId": str,
        "runId": str,
        "runUrl": str,
        "status": str,
        "startTime": str,
        "endTime": str,
        "elapsedTime": float,
        "traceId": str,
    },
)
