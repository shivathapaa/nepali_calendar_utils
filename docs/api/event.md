# Events, day status and working days

What a calendar has on a day, when an institution is closed, and the arithmetic that
counts the days it opens. No event data ships with the library by design; a consumer
plugs in a `NepaliEventProvider`.

## Events

```{eval-rst}
.. automodule:: nepali_calendar_utils.event.nepali_calendar_event
   :members:
   :show-inheritance:
```

## Provider SPI

```{eval-rst}
.. automodule:: nepali_calendar_utils.event.nepali_event_provider
   :members:
   :show-inheritance:
```

## Day status

```{eval-rst}
.. automodule:: nepali_calendar_utils.event.nepali_day_status
   :members:
   :show-inheritance:
```

## Calendar policy

```{eval-rst}
.. automodule:: nepali_calendar_utils.event.nepali_calendar_policy
   :members:
   :show-inheritance:
```

## Working-day helpers

```{eval-rst}
.. automodule:: nepali_calendar_utils.event.event_helpers
   :members:
   :show-inheritance:
```

## Former holiday names

Code written against the 3.0.0 holiday package keeps working, implementations of
`NepaliHolidayProvider` included. Importing from here raises a `DeprecationWarning`.

```{eval-rst}
.. automodule:: nepali_calendar_utils.holiday.holiday_provider
   :members:
   :show-inheritance:
```

```{eval-rst}
.. automodule:: nepali_calendar_utils.holiday.holiday_helpers
   :members:
   :show-inheritance:
```
