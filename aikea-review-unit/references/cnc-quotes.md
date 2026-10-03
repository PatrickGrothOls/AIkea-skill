# CNC quote requests

## Availability in this release

“Make it real” opens the quote preferences page with a preview of your design.
You can choose CNC machining, painting and installation preferences and return
to the design without losing those choices.

Customer CNC sending is not available yet: the hosted service deployment and
live sign-in/upload verification are deferred. Once available, it will require
an invitation. Installing the public skill does not activate this service.
Painting and installation choices are saved preferences only; this release does
not find tradespeople, contact them, place orders or take payment. Sending a CNC
quote request never approves manufacturing.

## Preparing a future invited submission

The native upload flow needs the skill runtime and your browser on the same
computer, with localhost port 8766 available. A model running in a remote cloud
container cannot complete this browser callback on your behalf.

Installation itself needs no Git. Sending editable source additionally requires
Git and an explicitly chosen design repository with a committed HEAD and a
project subdirectory. Keep that repository outside the replaceable installation.
Review its source snapshot and branch documentation before sending. The package
contains permitted source and docs plus a PNG preview, not STEP or other generated
geometry. The operator regenerates geometry from the source in an isolated review
environment; uploaded code remains untrusted.

After deployment, the operator supplies an invitation and a public configuration
file containing API/login URLs and a public client ID. Customers never supply
AWS keys. The assistant configures the normal viewer launch environment:

```sh
export AIKEA_CNC_GATEWAY_CONFIG=/absolute/path/to/outputs.json
export AIKEA_CNC_SOURCE_REPO=/absolute/path/to/design-repository
export AIKEA_CNC_PROJECT_PATH=assemblies/design-name
```

Use the normal verified viewer launch command. The person clicks “Sign in and
send CNC request,” signs in directly in the browser, then returns to the viewer
for the receipt. Passwords and tokens must never be copied into the conversation.
An error is not a receipt; retry only through the existing submission flow.
Until the operator confirms service availability, keep sending disabled.
