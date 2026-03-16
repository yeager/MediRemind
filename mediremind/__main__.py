"""Entry point for python3 -m mediremind."""

import sys

from mediremind.application import MediRemindApp


def main():
    app = MediRemindApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
