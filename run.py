import pytest
from loguru import logger
from auto_test.common.handle_path import log_path

logger.add(
    log_path,
    encoding="utf-8",
    level="DEBUG",
    rotation="10MB",
    retention=20,
)


pytest.main(['-s','-v','--alluredir=outputs/allure-results','--clean-alluredir'])