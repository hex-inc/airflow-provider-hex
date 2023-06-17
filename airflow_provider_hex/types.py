from typing import List

from typing_extensions import TypedDict

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

NotificationResponse = TypedDict(
    "NotificationResponse",
    {
        "type": str,
        "recipientType": str,
        "includeSuccessScreenshot": bool,
        "recipients": List[dict],
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
        "notifications": List[NotificationResponse],
    },
)


NotificationDetails = TypedDict(
    "NotificationDetails",
    {
        "type": str,
        "includeSuccessScreenshot": bool,
        "slackChannelIds": List[str],
        "userIds": List[str],
        "groupIds": List[str],
    },
)
