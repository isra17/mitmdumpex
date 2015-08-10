# mitmdumpex

Mitmdump tools with extended functionalities:

 * Split logs for each clients
 * Log rotation

Mitmdump parameters are all supported as well.

## Usage

 * `--split-flows [OUTDIR]`: Creates a dump file for each clients with their IP as the filename in `OUTDIR` folder.
 * `--rotate-logs`: Prefixes the logs with the current date (UTC) and rotate to a new file each days. Listen for signal USR1 to flush logs.

### Example

`mitmdumpex --split-flows dumps/ --rotate-logs` would output something like:
```
dumps/192.168.0.1/15-08-01
dumps/192.168.0.1/15-08-02
dumps/192.168.0.2/15-08-01
dumps/192.168.0.4/15-08-02
```

`--rotate-logs` can also be used with regular flow writer:

`mitmdumpex -w flows.dump --rotate-logs`
