import threading
import time
from typing import Generator

import pytest

from fleet_mix_app import create_app


@pytest.fixture(scope="session")
def app_server() -> Generator[str, None, None]:
    """Start the Flask app server for Playwright tests."""
    app = create_app()

    def run():
        app.run(
            host="127.0.0.1",
            port=5000,
            debug=False,
            use_reloader=False,
        )

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    time.sleep(3)
    yield "http://127.0.0.1:5000"
