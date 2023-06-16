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
        "recipients": list[dict],
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
        "notifications": list[NotificationResponse],
    },
)


NotificationDetails = TypedDict(
    "NotificationDetails",
    {
        "type": str,
        "includeSuccessScreenshot": bool,
        "slackChannelIds": list[str],
        "userIds": list[str],
        "groupIds": list[str],
    },
)
