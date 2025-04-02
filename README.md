# sysdiagnose-tools

Tools that you can use to explore a sysdiagnose on your Mac

[![Ubuntu Testing](https://github.com/riigess/sysdiagnose-tools/actions/workflows/ubuntu-tests.yml/badge.svg)](https://github.com/riigess/sysdiagnose-tools/actions/workflows/ubuntu-tests.yml)

## Sysdiagnose

### What is it?

A sysdiagnose is a system diagnostic taken by an Apple Device on the device representing the current state of the device. Typically, Apple and third-party developers use the sysdiagnose to understand why apps and services are not functioning as expected.

### How do I get a sysdiagnose?

Here's a very convenient link from Apple - https://it-training.apple.com/tutorials/support/sup075/. Once saved, the sysdiagnose is available by going to Settings > Privacy & Security > Analytics & Improvements > Analytics Data. The sysdiagnose name is saved as `sysdiagnose_date_time_OSName_DeviceName_buildIdentifier.tar.gz`. You should be able to export this file using the share button in the top-right after tapping on that file in Analytics Data.

You can also use a developer profile to export a sysdiagnose, but I will not be guiding or instructing anybody through said process as the former is simpler.

## Powerlogs

The current powerlogs are stored under <sysdiagnose_root>/logs/powerlogs/powerlog_date_time_randomId.plsql. This is a SQLite file with a ton of different tables. After diving deep, PLBatteryAgent_EventBackward_Battery is the table we look at for [charging/convert_powerlog_to_csv.py](src/sysdiagnose-tools/charging/convert_powerlog_to_csv.py).

The output from running the aforementioned script should include a datetime, battery %, RawLevel, battery voltage, estimated temperature, and actual temperature of the device overall. (Please note the actual temperature is specific to a single sensor, there are literally tons of sensors on the device I do not know which sensor this is sampling specifically, but I am assuming it's a battery temperature sensor.)
