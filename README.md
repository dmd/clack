Controller for the [KRUSH Flip Clock](https://www.krushflipclock.com/), a [flip disc display](https://en.wikipedia.org/wiki/Flip-disc_display).

Talk directly to the RS485 connection (remove the built in Photon controller).

send data via:

    curl  --data-urlencode "bitmap@filename" http://localhost:8080/clack/


The 'scroll' program lets you scroll abitrary text, optionally using X Windows BDF fonts 14 pixels or shorter.
