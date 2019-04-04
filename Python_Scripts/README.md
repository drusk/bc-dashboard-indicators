# Dashboard SQL Generator

## Usage

```bash
python3 generate_dashboard_sql.py
```

The path to the generated SQL will be printed.

## Configuration

Currently all configuration such as the names of the dashboards
to include and provider number are defined directly in the script
at the top of the file.

Any that need to change frequently should be extracted as command
line arguments or to a separate configuration file.

## Dependencies

Uses Python 3. No third party libraries are used.