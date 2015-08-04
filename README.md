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
dumps/150730-192.168.0.1
dumps/150802-192.168.0.1
dumps/150802-192.168.0.2
dumps/150803-192.168.0.1
dumps/150804-192.168.0.4
```

`--rotate-logs` can also be used with regular flow writer:

`mitmdumpex -w flows.dump --rotate-logs`
