"""
Reports functionality for the API
"""

import json
import inspect
import traceback
import logging

from .tg_bot import send as send_tg


with open('sets.json', 'r') as file:
    sets = json.loads(file.read())
    MODE = sets['mode']
    BUG_CHAT = sets['bug_chat']

SYMBOLS = ['💬', '🟢', '🟡', '🔴', '❗️', '✅', '🛎']
TYPES = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'IMPORTANT', 'REQUEST']


class Report():
    """ Report logs and notifications on Telegram chat or in log files """

    def __init__(self, mode):
        self.mode = mode

    def _report(self, text, type_=0, extra=None, tags=None):
        """ Make report message and send """

        if self.mode != 'PROD' and type_ == 0:
            return

        if not tags:
            tags = []

        previous = inspect.stack()[2]
        path = previous.filename.replace('/', '.').split('.')[2:-1]

        if path[0] == 'api':
            path = path[1:]

        if previous.function != 'handle':
            path.append(previous.function)

        path = '.'.join(path)

        text = f"{SYMBOLS[type_]} {MODE} {TYPES[type_]}" \
               f"\n{path}" \
               f"\n\n{text}"

        if extra:
            if isinstance(extra, dict):
                extra_text = "\n".join(f"{i} = {extra[i]}" for i in extra)
            else:
                extra_text = str(extra)

            text_with_extra = text + "\n\n" + extra_text
        else:
            text_with_extra = text

        tags = [self.mode.lower()] + tags
        outro = f"\n\n{previous.filename}:{previous.lineno}" \
                f"\n#" + " #".join(tags)

        text += outro
        text_with_extra += outro

        try:
            send_tg(BUG_CHAT, text_with_extra, markup=None)

        except Exception as e:
            if extra:
                logging.error(f"{SYMBOLS[3]}  Send report  {extra}")

                try:
                    send_tg(BUG_CHAT, text, markup=None)
                except Exception as e:
                    logging.error(f"{SYMBOLS[3]}  Send report  {type_} {text}")

            else:
                logging.error(f"{SYMBOLS[3]}  Send report  {type_} {text}")


    def debug(self, text, extra=None):
        """ Debug
        Sequence of function calls, internal values
        """

        logging.debug(f"{SYMBOLS[0]}  {text}  {json.dumps(extra)}")

    def info(self, text, extra=None, tags=None):
        """ Info
        System logs and event journal
        """

        logging.info(f"{SYMBOLS[1]}  {text}  {json.dumps(extra)}")
        self._report(text, 1, extra, tags)

    def warning(self, text, extra=None, tags=None):
        """ Warning
        Unexpected / strange code behavior that does not entail consequences
        """

        logging.warning(f"{SYMBOLS[2]}  {text}  {json.dumps(extra)}")
        self._report(text, 2, extra, tags)

    def error(self, text, extra=None, tags=None, error=None):
        """ Error
        An unhandled error occurred
        """

        content = (
            "".join(traceback.format_exception(None, error, error.__traceback__))
            if error is not None else
            f'{text}  {json.dumps(extra)}'
        )

        logging.error(f"{SYMBOLS[3]}  {content}")
        self._report(text, 3, extra, tags)

    def critical(self, text, extra=None, tags=None, error=None):
        """ Critical
        An error occurred that affects the operation of the service
        """

        content = (
            "".join(traceback.format_exception(None, error, error.__traceback__))
            if error is not None else
            f'{text}  {json.dumps(extra)}'
        )

        logging.critical(f"{SYMBOLS[4]}  {content}")
        self._report(text, 4, extra, tags)

    def important(self, text, extra=None, tags=None):
        """ Important
        Trigger on tracked user action was fired
        """

        logging.info(f"{SYMBOLS[5]}  {text}  {json.dumps(extra)}")
        self._report(text, 5, extra, tags)

    def request(self, text, extra=None, tags=None):
        """ Request
        The user made a request, the intervention of administrators is necessary
        """

        logging.info(f"{SYMBOLS[6]}  {text}  {json.dumps(extra)}")
        self._report(text, 6, extra, tags)


report = Report(MODE)
