Task 8 of 11 for "Bench Board": the Request page and its error, sending and done states. Use list_layers for ids (Nav, Field, Select, TextArea, DropZone, Button, Logo, Card, Drawer, Home). Desktop pages are 1440×1024 frames, fill bg, vertical auto layout, clip on, with a Nav instance (sizingH fill) on top.

1. "Request" at x 4920, y 1900 (Nav Page=Request). A vertical frame "header" (padding 48 80 24 80, gap 12, no fill) with "Request a test" (H1) and "Tell me what to run next on the GB10." (Body, muted). Then a vertical frame "form" (padding 8 80 48 80, gap 20, no fill) holding: Field instance named "field/Name" (label "Name", value "Your name"); Field instance "field/Email" (label "Email", value "you@example.com"); a horizontal frame "selects" (width 560, gap 20) with two Select instances that fill the width ("Model to test" / "e.g. Llama 5 8B" and "Hardware" / "NVIDIA DGX Spark GB10"); a TextArea instance; a DropZone instance; a Button instance named "send" with label "Send request".
2. "Request – error" at x 6560: duplicate Request, rename, set field/Name to State=Filled with value "Sam", field/Email to State=Error with value "sam@".
3. "Request – sending" at x 8200: duplicate the error page, rename, set field/Email to State=Filled with value "sam@example.com", and the send button to Type=Disabled with label "Sending…".
4. "Request – done" at x 9840: duplicate Request, rename, hide "form", and add a vertical frame "success" (padding 48 80, gap 16, no fill) with a 72×72 circle frame "tick" (radius 36, fill #4ade8022, centred) holding "✓" (H1 at size 40, colour good), "Thanks, it's on the list" (H2) and "I'll test it on a live stream or in a video." (Body, muted).

## Checks
- exists: Request, Request – error, Request – sending, Request – done
- in Request: header, form, field/Name, field/Email, selects, send
- in Request – error: field/Email, send
- in Request – sending: send
- in Request – done: success, tick
