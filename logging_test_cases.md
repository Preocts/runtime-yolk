# yolk.py Draft (logging)

Logging looks to be easier to make a part of Yolk rather than abstract. WIP

## Set logging level at root logger, do not impact existing handlers

Setup:

- Add logging with `DEBUG` logger

Expectations:

- A log handler to stderr will be applied to root logger
- root logger level will be set to `10` (`DEBUG`)
- Existing log handlers will not be impacted

`example.py`

```py
import logging

from runtime_yolk import Yolk

log = logging.getLogger(__name__)
Yolk().add_logging("DEBUG")

# Debug logging available
```

`example_alt.py`

```py
import logging

from runtime_yolk import Yolk

Yolk().add_logging("DEBUG")
log = logging.getLogger(__name__)
# Note inverted order

# Debug logging available
```

TODO:
- Test on AWS lambda - should behave similar to pytest environment (existing
  handlers)
