# Changelog
---
## [Unreleased]

### Added
-

### Changed
-

### Fixed

## [0.1.10] - 2024-09-09

### Added
- Enhanced retry mechanism for polling project status
- New `max_poll_retries` and `poll_retry_delay` parameters for `HexRunProjectOperator`
- New `run_status_with_retries` method in `HexHook`
- New `poll_project_status` method in `HexHook` with improved error handling

### Changed
- Improved error handling for API calls and status checks


## [0.1.9] - 2023-05-16

### Added

- Added support for [Hex Notifications](https://learn.hex.tech/docs/develop-logic/hex-api/api-reference#operation/RunProject)

-


## [0.1.8] - 2023-01-08

### Added

- Provider now supports Python 3.7 (@shannonchoang)

### Fixed

- Missing __init__.py file in operators folder (@josh-fell)


## [0.1.7] - 2022-11-08

### Fixed

- Input Parameters do not send null values to the api.

## [0.1.6] - 2022-09-27

### Added

- Input Parameters can now be templated with Jinja macros

## [0.1.3] - 2022-09-15

### Added

- Add Update Cache Parameter
- Add User Agent to requests

## [0.1.2]

### Added

- Handles a new terminal state: UNABLE_TO_ALLOCATE_KERNEL

## [0.1.1]

### Added

- Initial Release
